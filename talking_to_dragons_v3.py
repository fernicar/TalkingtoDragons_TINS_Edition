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

def generate_single_prompt(base_prompt, is_enhancement=True):
    """Generate a single enhanced prompt using Ollama"""
    
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

    # Generation system prompt (new)
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

    max_retries = 3  # Reduced from 5
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
            
            # Clean the output - remove think tags, explanations, and formatting
            clean_prompt = generated_text.strip()
            
            # Remove <think> blocks
            import re
            clean_prompt = re.sub(r'<think>.*?</think>', '', clean_prompt, flags=re.DOTALL)
            
            # Remove any remaining XML-like tags
            clean_prompt = re.sub(r'<[^>]+>', '', clean_prompt)
            
            # Remove common unwanted prefixes/phrases
            unwanted_phrases = [
                "Here's the enhanced prompt:",
                "Enhanced prompt:",
                "Prompt:",
                "The refined prompt is:",
                "Here is the enhanced version:",
                "Enhanced version:",
                "Here's a unique variation:",
                "Unique variation:",
                "Variation:"
            ]
            for phrase in unwanted_phrases:
                if clean_prompt.startswith(phrase):
                    clean_prompt = clean_prompt[len(phrase):].strip()
            
            # Convert to single line and clean spaces
            clean_prompt = " ".join(clean_prompt.split())
            
            # Check word count - REDUCED MINIMUM
            word_count = len(clean_prompt.split())
            
            # Check if complete (ends with proper punctuation)
            is_complete = clean_prompt.strip().endswith((".", "!", "?"))
            
            # Enforce hard 300-word limit
            if word_count > 300:
                # Trim to exactly 300 words
                words = clean_prompt.split()
                clean_prompt = " ".join(words[:300])
                # Ensure it ends properly
                if not clean_prompt.endswith((".", "!", "?")):
                    clean_prompt = clean_prompt.rstrip() + "."
                word_count = 300
            
            # Accept if within range and complete
            if word_count >= 225 and is_complete and word_count <= 300:
                return clean_prompt, word_count
            
            # Accept shorter prompts if they seem complete and reasonable
            if word_count >= 150 and is_complete and retries >= 1:
                return clean_prompt, word_count
            
            # Only retry if significantly incomplete or very short
            if retries < max_retries - 1:
                retries += 1
                if word_count < 150:
                    full_prompt = f"{system_prompt}\n\nInput: {base_prompt}\n\nExpand this response to be more detailed: {clean_prompt}"
                elif not is_complete:
                    # Don't retry for incomplete - just add a period
                    clean_prompt = clean_prompt.rstrip() + "."
                    return clean_prompt, word_count
                else:
                    # Good enough - don't retry
                    break
            else:
                break  # Max retries reached
                
        except Exception as e:
            retries += 1
            if retries == max_retries:
                return f"[Error generating prompt: {e}]", 0
    
    # Return what we have, even if not perfect
    return clean_prompt if 'clean_prompt' in locals() else "[Generation failed]", word_count if 'word_count' in locals() else 0

def process_prompts():
    """Main processing function"""
    if mode_var.get() == "enhance":
        # Enhancement mode
        input_content = input_text.get("1.0", tk.END).strip()
        if not input_content:
            messagebox.showwarning("Warning", "No input prompts to enhance")
            return
        
        input_prompts = [line.strip() for line in input_content.split('\n') if line.strip()]
        total_prompts = len(input_prompts)
        
    else:
        # Generation mode
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
        
        input_prompts = [theme] * total_prompts  # Use theme for all generations
    
    # Clear output
    output_text.delete("1.0", tk.END)
    
    # Setup logging
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
        
        # Add to output immediately
        if output_text.get("1.0", tk.END).strip():
            output_text.insert(tk.END, "\n")
        output_text.insert(tk.END, enhanced_prompt)
        
        logging.info(f"Processed prompt {i+1}: {word_count} words")
        root.update()
    
    update_status(f"Completed! Generated {len(enhanced_prompts)} enhanced prompts")
    logging.info(f"Processing completed. Generated {len(enhanced_prompts)} prompts")

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

# GUI Setup
root = tk.Tk()
root.title("Ollama Prompt Factory")
root.geometry("900x700")
root.configure(bg="#f0f0f0")

# Fetch models
fetch_ollama_models()

# Title
title_label = tk.Label(root, text="Ollama Prompt Factory", font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#2c3e50")
title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

# Mode Selection
mode_frame = tk.LabelFrame(root, text="Mode Selection", font=("Arial", 12), bg="#f0f0f0", fg="#2c3e50", padx=10, pady=10)
mode_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

mode_var = tk.StringVar(value="enhance")
tk.Radiobutton(mode_frame, text="Enhance Existing Prompts", variable=mode_var, value="enhance", 
               command=on_mode_change, bg="#f0f0f0", fg="#34495e").grid(row=0, column=0, padx=10, pady=5)
tk.Radiobutton(mode_frame, text="Generate New Prompts", variable=mode_var, value="generate", 
               command=on_mode_change, bg="#f0f0f0", fg="#34495e").grid(row=0, column=1, padx=10, pady=5)

# Enhancement Mode Frame
enhance_frame = tk.LabelFrame(root, text="Enhancement Mode", font=("Arial", 12), bg="#f0f0f0", fg="#2c3e50", padx=10, pady=10)
enhance_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

file_label = tk.Label(enhance_frame, text="No file loaded", bg="#f0f0f0", fg="#34495e")
file_label.grid(row=0, column=0, columnspan=2, pady=5)

tk.Button(enhance_frame, text="Load Prompt File", command=load_prompt_file, 
          bg="#3498db", fg="white", padx=10, pady=5).grid(row=1, column=0, padx=5, pady=5)

# Generation Mode Frame
generate_frame = tk.LabelFrame(root, text="Generation Mode", font=("Arial", 12), bg="#f0f0f0", fg="#2c3e50", padx=10, pady=10)

tk.Label(generate_frame, text="Theme/Style:", bg="#f0f0f0", fg="#34495e").grid(row=0, column=0, sticky="e", padx=5, pady=5)
theme_entry = tk.Entry(generate_frame, width=40, font=("Arial", 10))
theme_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(generate_frame, text="Number of prompts:", bg="#f0f0f0", fg="#34495e").grid(row=1, column=0, sticky="e", padx=5, pady=5)
count_entry = tk.Entry(generate_frame, width=10, font=("Arial", 10))
count_entry.insert(0, "50")
count_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)

# Model Selection
model_frame = tk.LabelFrame(root, text="Model Selection", font=("Arial", 12), bg="#f0f0f0", fg="#2c3e50", padx=10, pady=10)
model_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

tk.Label(model_frame, text="Ollama Model:", bg="#f0f0f0", fg="#34495e").grid(row=0, column=0, padx=5, pady=5)
model_var = tk.StringVar(value=available_models[0] if available_models else "gemma3:27b")
model_dropdown = ttk.Combobox(model_frame, textvariable=model_var, values=available_models, state="readonly", width=30)
model_dropdown.grid(row=0, column=1, padx=5, pady=5)

# Control Buttons
button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.grid(row=4, column=0, columnspan=2, pady=10)

tk.Button(button_frame, text="Process Prompts", command=process_prompts, 
          bg="#e74c3c", fg="white", padx=15, pady=8, font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Save Output", command=save_output_file, 
          bg="#27ae60", fg="white", padx=15, pady=8, font=("Arial", 10, "bold")).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Clear All", command=clear_all, 
          bg="#95a5a6", fg="white", padx=15, pady=8, font=("Arial", 10, "bold")).grid(row=0, column=2, padx=5)

# Input/Output Area
io_frame = tk.Frame(root, bg="#f0f0f0")
io_frame.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)

# Input Section
input_frame = tk.LabelFrame(io_frame, text="Input Prompts", font=("Arial", 12), bg="#f0f0f0", fg="#2c3e50", padx=5, pady=5)
input_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

input_text = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, width=40, height=15, 
                                       bg="white", fg="#2c3e50", font=("Arial", 10))
input_text.grid(row=0, column=0, sticky="nsew")

# Output Section
output_frame = tk.LabelFrame(io_frame, text="Enhanced Prompts", font=("Arial", 12), bg="#f0f0f0", fg="#2c3e50", padx=5, pady=5)
output_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, width=40, height=15, 
                                        bg="white", fg="#2c3e50", font=("Arial", 10))
output_text.grid(row=0, column=0, sticky="nsew")

# Status Area
status_frame = tk.LabelFrame(root, text="Status", font=("Arial", 12), bg="#f0f0f0", fg="#2c3e50", padx=10, pady=10)
status_frame.grid(row=6, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

status_text = tk.Text(status_frame, height=3, bg="#ecf0f1", fg="#2c3e50", font=("Arial", 10), state=tk.DISABLED)
status_text.grid(row=0, column=0, sticky="ew")

# Configure grid weights
root.grid_rowconfigure(5, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

io_frame.grid_rowconfigure(0, weight=1)
io_frame.grid_columnconfigure(0, weight=1)
io_frame.grid_columnconfigure(1, weight=1)

input_frame.grid_rowconfigure(0, weight=1)
input_frame.grid_columnconfigure(0, weight=1)
output_frame.grid_rowconfigure(0, weight=1)
output_frame.grid_columnconfigure(0, weight=1)

status_frame.grid_columnconfigure(0, weight=1)

# Initialize mode
on_mode_change()

# Initial status
update_status("Ready - Select mode and configure options")

root.mainloop()