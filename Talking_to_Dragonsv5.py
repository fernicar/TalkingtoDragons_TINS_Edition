import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk, messagebox
import requests
import json
import os
import logging

# Global variables
available_models = []

# Fetch available Ollama models
def fetch_ollama_models():
    global available_models
    try:
        response = requests.get("http://localhost:11434/api/tags")
        response.raise_for_status()
        data = response.json()
        available_models = [model["name"] for model in data.get("models", [])]
        if not available_models:
            available_models = ["gemma3:27b"]  # Fallback
    except Exception as e:
        print(f"Error fetching Ollama models: {e}")
        available_models = ["gemma3:27b"]  # Fallback if API fails
    return available_models

def update_status(message):
    status_text.config(state=tk.NORMAL)
    status_text.delete("1.0", tk.END)
    status_text.insert(tk.END, message)
    status_text.config(state=tk.DISABLED)
    root.update()

def load_prompt_file():
    file_path = filedialog.askopenfilename(
        title="Select Prompt File",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if file_path:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                input_prompts = [line.strip() for line in content.split('\n') if line.strip()]
                
            input_text.delete("1.0", tk.END)
            input_text.insert(tk.END, '\n'.join(input_prompts))
            
            file_label.config(text=f"Loaded: {os.path.basename(file_path)} ({len(input_prompts)} prompts)")
            mode_var.set("enhance")
            update_status(f"Loaded {len(input_prompts)} prompts for enhancement")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {e}")

def save_output_file():
    if not output_text.get("1.0", tk.END).strip():
        messagebox.showwarning("Warning", "No output to save")
        return
        
    file_path = filedialog.asksaveasfilename(
        title="Save Enhanced Prompts",
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if file_path:
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(output_text.get("1.0", tk.END).strip())
            update_status(f"Saved to: {os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")

def clean_prompt_output(generated_text, is_chinese=False):
    """Enhanced cleaning function for both English and Chinese outputs"""
    import re
    
    # Clean the output - remove think tags, explanations, and formatting
    clean_prompt = generated_text.strip()
    
    # Remove <think> blocks (existing functionality)
    clean_prompt = re.sub(r'<think>.*?</think>', '', clean_prompt, flags=re.DOTALL)
    
    # Remove any remaining XML-like tags (existing functionality)
    clean_prompt = re.sub(r'<[^>]+>', '', clean_prompt)
    
    # Remove Polaris thinking blocks - ENHANCED for your bleeding issues
    clean_prompt = re.sub(r'\*\*Thoughts:\*\*.*?(?=\*\*Prompt:\*\*|\*\*Summary:\*\*|\*\*Final Prompt:\*\*|$)', '', clean_prompt, flags=re.DOTALL)
    clean_prompt = re.sub(r'\*\*Summary:\*\*.*?(?=\*\*Prompt:\*\*|\*\*Final Prompt:\*\*|$)', '', clean_prompt, flags=re.DOTALL)
    clean_prompt = re.sub(r'Thoughts:.*?(?=Prompt:|Summary:|Final Prompt:|$)', '', clean_prompt, flags=re.DOTALL)
    clean_prompt = re.sub(r'Summary:.*?(?=Prompt:|Final Prompt:|$)', '', clean_prompt, flags=re.DOTALL)
    
    # Remove common unwanted prefixes/phrases (existing + enhanced)
    unwanted_phrases = [
        "Here's the enhanced prompt:",
        "Enhanced prompt:",
        "Prompt:",
        "**Prompt:**",
        "**Final Prompt:**",
        "Final Prompt:",
        "The refined prompt is:",
        "Here is the enhanced version:",
        "Enhanced version:",
        "Here's a unique variation:",
        "Unique variation:",
        "Variation:"
    ]
    
    # Add Chinese-specific unwanted phrases
    if is_chinese:
        unwanted_phrases.extend([
            "以下是增强后的提示词：",
            "增强提示词：",
            "提示词：",
            "改进后的提示词：",
            "这是独特的变体：",
            "变体：",
            "使用哈苏",
            "采用超现实主义数字艺术风格",
            "f/2.8",
            "ISO 100"
        ])
    
    for phrase in unwanted_phrases:
        if clean_prompt.startswith(phrase):
            clean_prompt = clean_prompt[len(phrase):].strip()
    
    # Handle Chinese truncation issues
    if is_chinese and clean_prompt.endswith('。') and len(clean_prompt) < 50:
        # Likely truncated, but keep what we have
        pass
    
    # Convert to single line and clean spaces
    clean_prompt = " ".join(clean_prompt.split())
    
    return clean_prompt

def generate_single_prompt(base_prompt, is_enhancement=True):
    """Generate a single enhanced prompt using Ollama (EXISTING ENGLISH FUNCTION)"""
    
    # Enhancement system prompt (existing)
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

    # Generation system prompt (existing)
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
        full_prompt = f"{system_prompt}\n\nInput prompt to enhance: {base_prompt}"
    else:
        system_prompt = generation_system_prompt
        full_prompt = f"{system_prompt}\n\nCore concept to create unique variation from: {base_prompt}"

    max_retries = 3
    retries = 0
    
    while retries < max_retries:
        try:
            request_json = {
                "model": model_var.get(),
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
            
            # Use enhanced cleaning function
            clean_prompt = clean_prompt_output(generated_text, is_chinese=False)
            
            # Check word count
            word_count = len(clean_prompt.split())
            
            # Check if complete (ends with proper punctuation)
            is_complete = clean_prompt.strip().endswith((".", "!", "?"))
            
            # Enforce hard 300-word limit
            if word_count > 300:
                words = clean_prompt.split()
                clean_prompt = " ".join(words[:300])
                if not clean_prompt.endswith((".", "!", "?")):
                    clean_prompt = clean_prompt.rstrip() + "."
                word_count = 300
            
            # Accept if within range and complete
            if word_count >= 225 and is_complete and word_count <= 300:
                return clean_prompt, word_count
            
            # Accept shorter prompts if they seem complete and reasonable
            if word_count >= 150 and is_complete and retries >= 1:
                return clean_prompt, word_count
            
            if retries < max_retries - 1:
                retries += 1
                if word_count < 150:
                    full_prompt = f"{system_prompt}\n\nInput: {base_prompt}\n\nExpand this response to be more detailed: {clean_prompt}"
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

def generate_chinese_prompt(base_prompt, is_enhancement=True):
    """Generate Chinese prompt - NEW FUNCTION for token efficiency"""
    
    # Chinese Enhancement system prompt
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

    # Chinese Generation system prompt
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
        full_prompt = f"{system_prompt}\n\n要增强的输入提示词: {base_prompt}"
    else:
        system_prompt = chinese_generation_system_prompt
        full_prompt = f"{system_prompt}\n\n要创建独特变体的核心概念: {base_prompt}"

    max_retries = 3
    retries = 0
    
    while retries < max_retries:
        try:
            request_json = {
                "model": model_var.get(),
                "prompt": full_prompt,
                "max_tokens": 300,  # Reduced for Chinese efficiency
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
            
            # Use enhanced cleaning function with Chinese flag
            clean_prompt = clean_prompt_output(generated_text, is_chinese=True)
            
            # Chinese character count (more meaningful than word count)
            char_count = len(clean_prompt.replace(" ", ""))
            
            # Check if complete
            is_complete = clean_prompt.strip().endswith(("。", "！", "？", ".", "!", "?"))
            
            # Enforce character limit for Chinese (150-200 chars is quite detailed)
            if char_count > 200:
                clean_prompt = clean_prompt[:200]
                if not clean_prompt.endswith(("。", "！", "？", ".", "!", "?")):
                    clean_prompt = clean_prompt.rstrip() + "。"
                char_count = len(clean_prompt.replace(" ", ""))
            
            # Accept if within range and complete
            if char_count >= 100 and is_complete and char_count <= 200:
                return clean_prompt, char_count
            
            # Accept shorter prompts if they seem complete
            if char_count >= 80 and is_complete and retries >= 1:
                return clean_prompt, char_count
            
            if retries < max_retries - 1:
                retries += 1
                if char_count < 80:
                    full_prompt = f"{system_prompt}\n\n输入: {base_prompt}\n\n请扩展这个回应，使其更详细: {clean_prompt}"
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

def process_prompts():
    """Main processing function - EXISTING ENGLISH PROCESSING"""
    if mode_var.get() == "enhance":
        input_content = input_text.get("1.0", tk.END).strip()
        if not input_content:
            messagebox.showwarning("Warning", "No input prompts to enhance")
            return
        
        input_prompts = [line.strip() for line in input_content.split('\n') if line.strip()]
        total_prompts = len(input_prompts)
        
    else:
        theme = theme_entry.get().strip()
        if not theme:
            messagebox.showwarning("Warning", "Please enter a theme/style for generation")
            return
        
        try:
            total_prompts = int(count_entry.get())
            if total_prompts <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Warning", "Please enter a valid number of prompts to generate")
            return
        
        input_prompts = [theme] * total_prompts
    
    output_text.delete("1.0", tk.END)
    
    log_file = "prompt_factory.log"
    logging.basicConfig(
        filename=log_file, 
        level=logging.INFO, 
        format="%(asctime)s - %(message)s",
        filemode='a'
    )
    
    update_status("Starting prompt processing...")
    logging.info(f"Starting processing of {total_prompts} prompts")
    
    enhanced_prompts = []
    
    for i, prompt in enumerate(input_prompts):
        update_status(f"Processing prompt {i+1}/{total_prompts}...")
        
        is_enhancement = mode_var.get() == "enhance"
        enhanced_prompt, word_count = generate_single_prompt(prompt, is_enhancement)
        
        enhanced_prompts.append(enhanced_prompt)
        
        if output_text.get("1.0", tk.END).strip():
            output_text.insert(tk.END, "\n")
        output_text.insert(tk.END, enhanced_prompt)
        
        logging.info(f"Processed prompt {i+1}: {word_count} words")
        root.update()
    
    update_status(f"Completed! Generated {len(enhanced_prompts)} enhanced prompts")
    logging.info(f"Processing completed. Generated {len(enhanced_prompts)} prompts")

def process_chinese_prompts():
    """Chinese processing function - NEW FUNCTION"""
    if mode_var.get() == "enhance":
        input_content = input_text.get("1.0", tk.END).strip()
        if not input_content:
            messagebox.showwarning("Warning", "No input prompts to enhance")
            return
        
        input_prompts = [line.strip() for line in input_content.split('\n') if line.strip()]
        total_prompts = len(input_prompts)
        
    else:
        theme = theme_entry.get().strip()
        if not theme:
            messagebox.showwarning("Warning", "Please enter a theme/style for generation")
            return
        
        try:
            total_prompts = int(count_entry.get())
            if total_prompts <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Warning", "Please enter a valid number of prompts to generate")
            return
        
        input_prompts = [theme] * total_prompts
    
    output_text.delete("1.0", tk.END)
    
    log_file = "prompt_factory_chinese.log"
    logging.basicConfig(
        filename=log_file, 
        level=logging.INFO, 
        format="%(asctime)s - %(message)s",
        filemode='a'
    )
    
    update_status("Starting Chinese prompt processing...")
    logging.info(f"Starting Chinese processing of {total_prompts} prompts")
    
    enhanced_prompts = []
    
    for i, prompt in enumerate(input_prompts):
        update_status(f"Processing Chinese prompt {i+1}/{total_prompts}...")
        
        is_enhancement = mode_var.get() == "enhance"
        enhanced_prompt, char_count = generate_chinese_prompt(prompt, is_enhancement)
        
        enhanced_prompts.append(enhanced_prompt)
        
        if output_text.get("1.0", tk.END).strip():
            output_text.insert(tk.END, "\n")
        output_text.insert(tk.END, enhanced_prompt)
        
        logging.info(f"Processed Chinese prompt {i+1}: {char_count} characters")
        root.update()
    
    update_status(f"Completed! Generated {len(enhanced_prompts)} Chinese prompts")
    logging.info(f"Chinese processing completed. Generated {len(enhanced_prompts)} prompts")

def clear_all():
    """Clear all text areas"""
    input_text.delete("1.0", tk.END)
    output_text.delete("1.0", tk.END)
    file_label.config(text="No file loaded")
    update_status("Cleared all content")

def on_mode_change():
    """Handle mode selection changes"""
    if mode_var.get() == "enhance":
        enhance_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        generate_frame.grid_remove()
    else:
        generate_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        enhance_frame.grid_remove()

# GUI Setup - DRAGON DIFFUSION BRANDING
root = tk.Tk()
root.title("Dragon Diffusion - Talking to Dragons")
root.geometry("1000x800")  # Reasonable default size
root.minsize(900, 700)     # Smaller minimum to fit more screens

# Welsh Dragon Colour Scheme - DEFINE BEFORE USE
BG_BLACK = "#0d0d0d"
BG_CHARCOAL = "#1a1a1a"
SCARLET_RED = "#dc143c"
RICH_GOLD = "#ffd700"
DARK_GOLD = "#b8860b"
TEXT_WHITE = "#ffffff"
TEXT_SILVER = "#c0c0c0"

root.configure(bg=BG_BLACK)

# Configure ttk styles for Dragon theme
style = ttk.Style()
style.theme_use('clam')
style.configure('Dragon.TCombobox', 
                fieldbackground=BG_CHARCOAL,
                background=BG_CHARCOAL,
                foreground=TEXT_WHITE,
                bordercolor=RICH_GOLD,
                arrowcolor=SCARLET_RED)

# Create main canvas with scrollbar for entire window
main_canvas = tk.Canvas(root, bg=BG_BLACK)
main_scrollbar = ttk.Scrollbar(root, orient="vertical", command=main_canvas.yview)
scrollable_frame = tk.Frame(main_canvas, bg=BG_BLACK)

scrollable_frame.bind(
    "<Configure>",
    lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
)

main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
main_canvas.configure(yscrollcommand=main_scrollbar.set)

# Pack canvas and scrollbar
main_canvas.pack(side="left", fill="both", expand=True)
main_scrollbar.pack(side="right", fill="y")

# Mouse wheel scrolling
def _on_mousewheel(event):
    main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

main_canvas.bind_all("<MouseWheel>", _on_mousewheel)

fetch_ollama_models()

# Title with Dragon Diffusion branding
title_frame = tk.Frame(scrollable_frame, bg=BG_BLACK)
title_frame.grid(row=0, column=0, columnspan=2, pady=(15, 25))

title_label = tk.Label(title_frame, text="Dragon Diffusion", 
                       font=("Arial", 20, "bold"), 
                       bg=BG_BLACK, fg=RICH_GOLD)
title_label.pack()

subtitle_label = tk.Label(title_frame, text="Talking to Dragons", 
                          font=("Arial", 14, "italic"), 
                          bg=BG_BLACK, fg=SCARLET_RED)
subtitle_label.pack()

tagline_label = tk.Label(title_frame, text="Professional Prompt Enhancement Suite", 
                         font=("Arial", 10), 
                         bg=BG_BLACK, fg=TEXT_SILVER)
tagline_label.pack(pady=(5, 0))

# Mode Selection with Dragon styling
mode_frame = tk.LabelFrame(scrollable_frame, text="Processing Mode", 
                           font=("Arial", 12, "bold"), 
                           bg=BG_BLACK, fg=RICH_GOLD, 
                           bd=2, relief="ridge")
mode_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=15, pady=10)

mode_var = tk.StringVar(value="enhance")
enhance_radio = tk.Radiobutton(mode_frame, text="Enhance Existing Prompts", 
                               variable=mode_var, value="enhance", 
                               command=on_mode_change, 
                               bg=BG_BLACK, fg=TEXT_WHITE, 
                               selectcolor=BG_CHARCOAL,
                               activebackground=BG_BLACK,
                               activeforeground=SCARLET_RED,
                               font=("Arial", 11))
enhance_radio.grid(row=0, column=0, padx=20, pady=10, sticky="w")

generate_radio = tk.Radiobutton(mode_frame, text="Generate New Variations", 
                                variable=mode_var, value="generate", 
                                command=on_mode_change, 
                                bg=BG_BLACK, fg=TEXT_WHITE, 
                                selectcolor=BG_CHARCOAL,
                                activebackground=BG_BLACK,
                                activeforeground=SCARLET_RED,
                                font=("Arial", 11))
generate_radio.grid(row=0, column=1, padx=20, pady=10, sticky="w")

# Enhancement Mode Frame
enhance_frame = tk.LabelFrame(scrollable_frame, text="Enhancement Mode", 
                              font=("Arial", 12, "bold"), 
                              bg=BG_BLACK, fg=RICH_GOLD, 
                              bd=2, relief="ridge")
enhance_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=15, pady=10)

file_label = tk.Label(enhance_frame, text="No file loaded", 
                      bg=BG_BLACK, fg=TEXT_SILVER, font=("Arial", 10))
file_label.grid(row=0, column=0, columnspan=2, pady=10)

load_btn = tk.Button(enhance_frame, text="Load Prompt File", 
                     command=load_prompt_file, 
                     bg=SCARLET_RED, fg=TEXT_WHITE, 
                     font=("Arial", 11, "bold"),
                     relief="raised", bd=2,
                     activebackground=DARK_GOLD,
                     activeforeground=BG_BLACK,
                     padx=20, pady=8)
load_btn.grid(row=1, column=0, padx=10, pady=10)

# Generation Mode Frame
generate_frame = tk.LabelFrame(scrollable_frame, text="Generation Mode", 
                               font=("Arial", 12, "bold"), 
                               bg=BG_BLACK, fg=RICH_GOLD, 
                               bd=2, relief="ridge")

theme_label = tk.Label(generate_frame, text="Theme/Style:", 
                       bg=BG_BLACK, fg=TEXT_WHITE, font=("Arial", 11))
theme_label.grid(row=0, column=0, sticky="e", padx=10, pady=10)

theme_entry = tk.Entry(generate_frame, width=50, font=("Arial", 11),
                       bg=BG_CHARCOAL, fg=TEXT_WHITE, 
                       insertbackground=SCARLET_RED,
                       relief="solid", bd=1)
theme_entry.grid(row=0, column=1, padx=10, pady=10)

count_label = tk.Label(generate_frame, text="Number of prompts:", 
                       bg=BG_BLACK, fg=TEXT_WHITE, font=("Arial", 11))
count_label.grid(row=1, column=0, sticky="e", padx=10, pady=10)

count_entry = tk.Entry(generate_frame, width=15, font=("Arial", 11),
                       bg=BG_CHARCOAL, fg=TEXT_WHITE, 
                       insertbackground=SCARLET_RED,
                       relief="solid", bd=1)
count_entry.insert(0, "50")
count_entry.grid(row=1, column=1, sticky="w", padx=10, pady=10)

# Model Selection with Dragon styling
model_frame = tk.LabelFrame(scrollable_frame, text="Model Selection", 
                            font=("Arial", 12, "bold"), 
                            bg=BG_BLACK, fg=RICH_GOLD, 
                            bd=2, relief="ridge")
model_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=15, pady=10)

model_label = tk.Label(model_frame, text="Ollama Model:", 
                       bg=BG_BLACK, fg=TEXT_WHITE, font=("Arial", 11))
model_label.grid(row=0, column=0, padx=15, pady=15)

model_var = tk.StringVar(value=available_models[0] if available_models else "gemma3:27b")
model_dropdown = ttk.Combobox(model_frame, textvariable=model_var, 
                              values=available_models, state="readonly", 
                              width=35, font=("Arial", 11),
                              style='Dragon.TCombobox')
model_dropdown.grid(row=0, column=1, padx=15, pady=15)

# Control Buttons with Dragon styling
button_frame = tk.Frame(scrollable_frame, bg=BG_BLACK)
button_frame.grid(row=4, column=0, columnspan=2, pady=20)

# Main processing buttons
process_btn = tk.Button(button_frame, text="Process English Prompts", 
                        command=process_prompts, 
                        bg=SCARLET_RED, fg=TEXT_WHITE, 
                        font=("Arial", 12, "bold"),
                        relief="raised", bd=3,
                        activebackground=DARK_GOLD,
                        activeforeground=BG_BLACK,
                        padx=20, pady=10)
process_btn.grid(row=0, column=0, padx=10)

save_btn = tk.Button(button_frame, text="Save Output", 
                     command=save_output_file, 
                     bg=RICH_GOLD, fg=BG_BLACK, 
                     font=("Arial", 12, "bold"),
                     relief="raised", bd=3,
                     activebackground=SCARLET_RED,
                     activeforeground=TEXT_WHITE,
                     padx=20, pady=10)
save_btn.grid(row=0, column=1, padx=10)

clear_btn = tk.Button(button_frame, text="Clear All", 
                      command=clear_all, 
                      bg=BG_CHARCOAL, fg=TEXT_WHITE, 
                      font=("Arial", 12, "bold"),
                      relief="raised", bd=3,
                      activebackground=SCARLET_RED,
                      activeforeground=TEXT_WHITE,
                      padx=20, pady=10)
clear_btn.grid(row=0, column=2, padx=10)

# Chinese processing button (functionality preserved, UI cleaned)
chinese_btn = tk.Button(button_frame, text="Process Chinese", 
                        command=process_chinese_prompts, 
                        bg="#8B4513", fg=TEXT_WHITE, 
                        font=("Arial", 11, "bold"),
                        relief="raised", bd=2,
                        activebackground=RICH_GOLD,
                        activeforeground=BG_BLACK,
                        padx=15, pady=8)
chinese_btn.grid(row=1, column=0, padx=10, pady=(10, 0))

chinese_note = tk.Label(button_frame, text="↑ Token-efficient Chinese output", 
                        bg=BG_BLACK, fg="#CD853F", 
                        font=("Arial", 9, "italic"))
chinese_note.grid(row=1, column=1, columnspan=2, sticky="w", padx=10, pady=(10, 0))

# Input/Output Area with Dragon styling - SCROLLABLE VERSION
io_frame = tk.Frame(scrollable_frame, bg=BG_BLACK)
io_frame.grid(row=5, column=0, columnspan=2, sticky="ew", padx=15, pady=15)

# Input Section - FIXED HEIGHT
input_frame = tk.LabelFrame(io_frame, text="Input Prompts", 
                            font=("Arial", 12, "bold"), 
                            bg=BG_BLACK, fg=RICH_GOLD, 
                            bd=2, relief="ridge")
input_frame.grid(row=0, column=0, sticky="ew", padx=(0, 8), pady=5)

input_text = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, 
                                       width=50, height=15, 
                                       bg=BG_CHARCOAL, fg=TEXT_WHITE, 
                                       font=("Consolas", 9),
                                       insertbackground=SCARLET_RED,
                                       selectbackground=SCARLET_RED,
                                       selectforeground=TEXT_WHITE,
                                       relief="solid", bd=1)
input_text.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

# Output Section - FIXED HEIGHT
output_frame = tk.LabelFrame(io_frame, text="Enhanced Prompts", 
                             font=("Arial", 12, "bold"), 
                             bg=BG_BLACK, fg=RICH_GOLD, 
                             bd=2, relief="ridge")
output_frame.grid(row=0, column=1, sticky="ew", padx=(8, 0), pady=5)

output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, 
                                        width=50, height=15, 
                                        bg=BG_CHARCOAL, fg=TEXT_WHITE, 
                                        font=("Consolas", 9),
                                        insertbackground=SCARLET_RED,
                                        selectbackground=SCARLET_RED,
                                        selectforeground=TEXT_WHITE,
                                        relief="solid", bd=1)
output_text.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

# Status Area with Dragon styling
status_frame = tk.LabelFrame(scrollable_frame, text="Status", 
                             font=("Arial", 12, "bold"), 
                             bg=BG_BLACK, fg=RICH_GOLD, 
                             bd=2, relief="ridge")
status_frame.grid(row=6, column=0, columnspan=2, sticky="ew", padx=15, pady=(10, 15))

status_text = tk.Text(status_frame, height=3, 
                      bg=BG_CHARCOAL, fg=RICH_GOLD, 
                      font=("Arial", 10), 
                      state=tk.DISABLED,
                      relief="solid", bd=1)
status_text.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

# Configure grid weights for the scrollable frame
scrollable_frame.grid_columnconfigure(0, weight=1)
scrollable_frame.grid_columnconfigure(1, weight=1)

io_frame.grid_columnconfigure(0, weight=1)
io_frame.grid_columnconfigure(1, weight=1)

input_frame.grid_columnconfigure(0, weight=1)
output_frame.grid_columnconfigure(0, weight=1)
status_frame.grid_columnconfigure(0, weight=1)

# Initialize mode
on_mode_change()

# Initial status with Dragon flair
update_status("Dragon Diffusion ready - Select processing mode and configure options")

root.mainloop()