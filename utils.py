import re

def clean_prompt_output(generated_text, is_chinese=False):
    """Enhanced cleaning function for both English and Chinese outputs"""

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
