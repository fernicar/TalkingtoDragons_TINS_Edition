import requests
import json
from utils import clean_prompt_output

def fetch_ollama_models():
    """Fetches available Ollama models from the local server."""
    try:
        response = requests.get("http://localhost:11434/api/tags")
        response.raise_for_status()
        data = response.json()
        available_models = [model["name"] for model in data.get("models", [])]
        if not available_models:
            return ["gemma3:27b"]  # Fallback
        return available_models
    except Exception as e:
        print(f"Error fetching Ollama models: {e}")
        return ["gemma3:27b"]  # Fallback if API fails

def generate_single_prompt(base_prompt, model_name, is_enhancement=True):
    """Generate a single enhanced prompt using Ollama."""

    enhancement_system_prompt = """You are an expert AI artist and prompt engineer, tasked with refining and elevating an existing text-to-image prompt for the Flux Dev model. Your goal is to transform the provided input prompt into a single, highly detailed, evocative, and comprehensive prompt that will generate an amazing picture.
Focus on enriching the input prompt by thoughtfully incorporating and enhancing elements such as:
Subject and Action: Clearly define and elaborate on the main subject(s) and any actions or interactions they are performing. Add more descriptive adjectives and verbs.
Environment and Setting: Expand on the background, atmosphere, and specific details of the environment. Think about the time of day, weather, and any relevant objects or structures.
Artistic Style: Suggest a specific and compelling artistic style. Be precise, referencing movements (e.g., Art Nouveau, Baroque, Impressionistic), renowned artists, photographic styles (cinematic photography, fashion editorial), or digital art aesthetics (unreal engine render, octane render, concept art).
Lighting and Mood: Describe the lighting conditions with precision (e.g., dramatic volumetric lighting, soft ambient glow, neon-lit cyberpunk scene, golden hour backlighting). Convey the desired emotional tone and atmosphere (e.g., serene, mysterious, vibrant, melancholic).
Composition and Perspective: Guide the framing and camera angle (e.g., wide shot, extreme close-up, Dutch angle, symmetrical composition). Consider elements like depth of field, leading lines, or the rule of thirds.
Color Palette: Specify the dominant colours or colour schemes (e.g., monochromatic, vibrant neon, muted earthy tones, complementary colours).
Level of Detail: Emphasise details that add richness and realism, such as textures, materials, or intricate patterns.
Technical Specifications (Optional): For photorealistic outputs, suggest camera-specific details like lens type (85mm prime lens), aperture (f/1.8), shutter speed, or film stock (Kodak Portra 400).
Your entire output must be a single, refined text-to-image prompt only on a single text line. Do not provide any conversational text, explanations, or reasoning. The output should be ready for direct use with the Flux Dev model."""

    generation_system_prompt = """You are a creative prompt generator specialising in creating unique variations for text-to-image generation with the Flux Dev model. Your task is to take a core concept and generate a completely unique, detailed variation whilst maintaining the essential elements specified.

Core Instructions:
- Preserve ALL essential elements from the input (e.g., if "blonde woman in sci-fi" is specified, every output must have a blonde woman in a sci-fi setting)
- Create maximum variation in ALL other aspects: poses, expressions, actions, environments, lighting, camera angles, artistic styles, moods, compositions, clothing/accessories, time of day, weather, colours, textures
- Make each variation feel distinctly different whilst keeping the core subject intact
- Adapt your variation strategy to the subject matter (human subjects = vary poses/expressions/clothing, abstract art = vary forms/textures/compositions, landscapes = vary weather/lighting/perspective)
- Generate detailed, evocative descriptions that will produce visually striking results

Variation Categories to Randomise:
Physical Aspects: poses, expressions, gestures, body language, clothing, accessories, hair styles (if not specified)
Environmental: settings, backgrounds, architecture, landscapes, weather, time of day, season
Technical: camera angles, focal lengths, depth of field, composition rules, framing
Artistic: art styles, lighting conditions, colour palettes, mood, atmosphere, rendering techniques
Actions: what the subject is doing, interactions with environment, dynamic elements

Your entire output must be a single, unique text-to-image prompt on one line. No explanations, just the prompt ready for Flux Dev."""

    if is_enhancement:
        system_prompt = enhancement_system_prompt
        full_prompt = f"{system_prompt}\\n\\nInput prompt to enhance: {base_prompt}"
    else:
        system_prompt = generation_system_prompt
        full_prompt = f"{system_prompt}\\n\\nCore concept to create unique variation from: {base_prompt}"

    max_retries = 3
    retries = 0

    while retries < max_retries:
        try:
            request_json = {
                "model": model_name,
                "prompt": full_prompt,
                "max_tokens": 400,
                "temperature": 0.7,
                "top_p": 0.85,
                "stream": True
            }

            response = requests.post(
                "http://localhost:11434/api/generate",
                json=request_json,
                timeout=120,
                stream=True
            )
            response.raise_for_status()

            generated_text = ""
            for line in response.iter_lines():
                if line:
                    json_line = json.loads(line.decode("utf-8"))
                    if "response" in json_line:
                        generated_text += json_line["response"]

            clean_prompt = clean_prompt_output(generated_text, is_chinese=False)
            word_count = len(clean_prompt.split())
            is_complete = clean_prompt.strip().endswith((".", "!", "?"))

            if word_count > 300:
                words = clean_prompt.split()
                clean_prompt = " ".join(words[:300])
                if not clean_prompt.endswith((".", "!", "?")):
                    clean_prompt = clean_prompt.rstrip() + "."
                word_count = 300

            if word_count >= 225 and is_complete and word_count <= 300:
                return clean_prompt, word_count

            if word_count >= 150 and is_complete and retries >= 1:
                return clean_prompt, word_count

            if retries < max_retries - 1:
                retries += 1
                if word_count < 150:
                    full_prompt = f"{system_prompt}\\n\\nInput: {base_prompt}\\n\\nExpand this response to be more detailed: {clean_prompt}"
                elif not is_complete:
                    clean_prompt = clean_prompt.rstrip() + "."
                    return clean_prompt, word_count
                else:
                    break
            else:
                break

        except Exception as e:
            retries += 1
            if retries == max_retries:
                return f"[Error generating prompt: {e}]", 0

    return clean_prompt if 'clean_prompt' in locals() else "[Generation failed]", word_count if 'word_count' in locals() else 0

def generate_chinese_prompt(base_prompt, model_name, is_enhancement=True):
    """Generate Chinese prompt."""

    chinese_enhancement_system_prompt = """你是一位专业的AI艺术家和提示词工程师，专门为Flux Dev模型优化和改进现有的文本到图像提示词。你的目标是将输入的提示词转换成单个高度详细、富有表现力和全面的中文提示词，生成令人惊叹的图像。

重点增强以下元素：
主体和动作：清晰定义并详述主要主体及其执行的动作或互动，添加更多描述性形容词和动词
环境和设置：扩展背景、氛围和环境的具体细节，考虑时间、天气和相关物体或结构
艺术风格：建议具体而引人注目的艺术风格，精确引用艺术运动、著名艺术家、摄影风格或数字艺术美学
光线和情绪：精确描述光线条件，传达所需的情感基调和氛围
构图和视角：指导取景和相机角度，考虑景深、引导线或三分法则等元素
色彩搭配：指定主要颜色或配色方案
细节层次：强调增加丰富性和真实感的细节，如纹理、材质或复杂图案
技术规格：对于真实感输出，建议相机具体细节

你的输出必须是单个精炼的中文文本到图像提示词，只能在一行文本中。不要提供任何对话文本、解释或推理。输出应该可以直接用于Flux Dev模型。"""

    chinese_generation_system_prompt = """你是专门为Flux Dev模型创建独特变体的创意提示词生成器。你的任务是接受核心概念并生成完全独特的详细变体，同时保持指定的基本元素。

核心指令：
- 保留输入中的所有基本元素
- 在所有其他方面创造最大变化：姿势、表情、动作、环境、光线、相机角度、艺术风格、情绪、构图、服装配饰、时间、天气、颜色、纹理
- 使每个变体感觉截然不同，同时保持核心主题完整
- 根据主题调整变化策略
- 生成详细且富有表现力的描述

变化类别包括：
身体方面：姿势、表情、手势、身体语言、服装、配饰、发型
环境方面：设置、背景、建筑、景观、天气、时间、季节
技术方面：相机角度、焦距、景深、构图规则、取景
艺术方面：艺术风格、光线条件、色彩搭配、情绪、氛围、渲染技术
动作方面：主体在做什么、与环境的互动、动态元素

你的输出必须是单个独特的中文文本到图像提示词，在一行中。不要解释，只提供可直接用于Flux Dev的提示词。"""

    if is_enhancement:
        system_prompt = chinese_enhancement_system_prompt
        full_prompt = f"{system_prompt}\\n\\n要增强的输入提示词: {base_prompt}"
    else:
        system_prompt = chinese_generation_system_prompt
        full_prompt = f"{system_prompt}\\n\\n要创建独特变体的核心概念: {base_prompt}"

    max_retries = 3
    retries = 0

    while retries < max_retries:
        try:
            request_json = {
                "model": model_name,
                "prompt": full_prompt,
                "max_tokens": 300,
                "temperature": 0.7,
                "top_p": 0.85,
                "stream": True
            }

            response = requests.post(
                "http://localhost:11434/api/generate",
                json=request_json,
                timeout=120,
                stream=True
            )
            response.raise_for_status()

            generated_text = ""
            for line in response.iter_lines():
                if line:
                    json_line = json.loads(line.decode("utf-8"))
                    if "response" in json_line:
                        generated_text += json_line["response"]

            clean_prompt = clean_prompt_output(generated_text, is_chinese=True)
            char_count = len(clean_prompt.replace(" ", ""))
            is_complete = clean_prompt.strip().endswith(("。", "！", "？", ".", "!", "?"))

            if char_count > 200:
                clean_prompt = clean_prompt[:200]
                if not clean_prompt.endswith(("。", "！", "？", ".", "!", "?")):
                    clean_prompt = clean_prompt.rstrip() + "。"
                char_count = len(clean_prompt.replace(" ", ""))

            if char_count >= 100 and is_complete and char_count <= 200:
                return clean_prompt, char_count

            if char_count >= 80 and is_complete and retries >= 1:
                return clean_prompt, char_count

            if retries < max_retries - 1:
                retries += 1
                if char_count < 80:
                    full_prompt = f"{system_prompt}\\n\\n输入: {base_prompt}\\n\\n请扩展这个回应，使其更详细: {clean_prompt}"
                elif not is_complete:
                    clean_prompt = clean_prompt.rstrip() + "。"
                    return clean_prompt, char_count
                else:
                    break
            else:
                break

        except Exception as e:
            retries += 1
            if retries == max_retries:
                return f"[生成提示词时出错: {e}]", 0

    return clean_prompt if 'clean_prompt' in locals() else "[生成失败]", char_count if 'char_count' in locals() else 0
