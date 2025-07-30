# 🐲 Prompt Writer - Talking to Dragons 🐲

Welcome, brave digital alchemists and prompt enchanters! Ever felt like your image generation prompts were more like whimpers than roars? Fear not! **Prompt Writer - Talking to Dragons** is here to transform your measly prompt scraps into magnificent, fire-breathing descriptions that'll make even the most stubborn AI dragons sit up and pay attention! ✨

This mystical Tkinter application harnesses the power of local Ollama models to take your basic prompts and enhance them into rich, detailed masterpieces worthy of the finest image generation spells. Say goodbye to bland "cat on beach" prompts and hello to epic 250-300 word sagas!

## 🌟 What Does This Dragon Do? 🌟

Transform your prompts from this:
```
A bioluminescent mushroom forest inhabited by miniature clockwork dragons
```

Into THIS legendary tome:
```
A bioluminescent mushroom forest at twilight, where towering, iridescent fungi emit soft cerulean and emerald glows under a misty, ethereal atmosphere, inhabited by miniature clockwork dragons with gilded, ornate bodies, intricate brass gears, and delicate, mechanical wings, their movements synchronized to the rhythmic pulse of the glowing forest, rendered in a hyper-detailed Art Nouveau style inspired by Gustav Klimt's flowing lines...
```

**Two Magical Modes:**
- 🔮 **Enhancement Mode**: Feed it your existing prompt lists and watch them grow into detailed epics
- ⚡ **Generation Mode**: Give it a theme ("Lovecraftian horror with tentacles and dread") and it'll spawn fresh prompts from the void

## 🧙‍♂️ Prerequisites - Gathering Your Magical Components 🧙‍♀️

Before we unleash this prompt-enhancing dragon, you'll need these mystical ingredients:

### 1. Ollama - The Dragon's Brain 🧠
This application speaks directly to local Ollama models, so you'll need Ollama installed and running:

- Download from [Ollama's official lair](https://ollama.ai/)
- Install a model (we recommend `gemma3:27b` for best results)
- Ensure it's running on `http://localhost:11434`

Test your setup:
```bash
ollama list
```

### 2. Python Environment 🐍
Create a virtual environment to keep your spells organised:

```bash
python -m venv venv
```

**On Windows:**
```bash
.\venv\Scripts\activate
```

**On macOS/Linux:**
```bash
source venv/bin/activate
```

## 🚀 Installation - Summoning the Dragon 🚀

1. **Clone the Dragon's Lair:**
   ```bash
   git clone https://github.com/yourusername/prompt-writer-talking-to-dragons.git
   cd prompt-writer-talking-to-dragons
   ```

2. **Install the Mystical Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Unleash the Dragon:**
   ```bash
   python ollama_prompt_factory.py
   ```

The GUI will materialise before your very eyes, ready to transform your prompts!

## 🎯 How to Wield This Magical Tool 🎯

### Enhancement Mode (Transform Existing Prompts)
1. **Load Your Prompt Scroll**: Click "Load Prompt File" and select your `.txt` file
   - **CRITICAL**: One prompt per line! No empty lines, no spaces, just pure prompt goodness
   - Example format:
     ```
     A cat sitting on a beach
     A dragon flying over mountains
     A wizard casting spells
     ```

2. **Choose Your Model**: Select your preferred Ollama model from the dropdown

3. **Process the Magic**: Hit "Process Prompts" and watch as each line transforms into a 250-300 word masterpiece

4. **Save Your Enhanced Tome**: Click "Save Output" to preserve your enhanced prompts

### Generation Mode (Create New Prompts)
1. **Select Generation Mode**: Choose the "Generate New Prompts" radio button

2. **Describe Your Vision**: Enter a theme like:
   - "Cyberpunk cityscapes with neon and rain"
   - "Lovecraftian horror with tentacles and cosmic dread"
   - "Steampunk airships in cloudy skies"

3. **Set Your Quantity**: Default is 50 prompts (adjustable)

4. **Let the Dragon Create**: Hit "Process Prompts" and watch new prompts materialise from the ether

## ⚠️ Dragon Warnings & Wisdom ⚠️

- **Sparse Input = Longer Processing**: Basic prompts like "girl on beach" will trigger retry logic as the system works harder to reach the 250-300 word target
- **Detailed Input = Lightning Fast**: Already-decent prompts will process quickly since they need less enhancement
- **One Prompt Per Line**: Your prompt injector demands this format - no exceptions!
- **Clean Output Guaranteed**: The system strips all `<think>` tags, XML artifacts, and unwanted prefixes

## 🔧 Technical Sorcery 🔧

### The Enhancement Spell
Each prompt undergoes this magical transformation:
1. **System Prompt Invocation**: Uses a specialised Flux-focused enhancement spell
2. **Word Count Validation**: Ensures 250-300 words using retry logic (just like our novel writer)
3. **Output Purification**: Strips LLM reasoning artifacts and unwanted formatting
4. **Single-Line Formatting**: Perfect for downstream prompt injection

### Retry Logic
- **Target Range**: 250-300 words (avoids infinite retry loops)
- **Max Attempts**: 5 retries per prompt
- **Smart Continuation**: Failed attempts continue from previous output
- **Graceful Fallback**: Accepts result even if not perfect after max retries

## 📁 File Formats 📁

**Input File Format** (one prompt per line):
```
A magical forest with glowing mushrooms
A steampunk laboratory with brass instruments
A cyberpunk street with neon advertisements
```

**Output Format** (ready for prompt injection):
```
A magical forest bathed in ethereal twilight, where bioluminescent mushrooms cast prismatic glows across moss-covered ground, their caps shimmering with otherworldly radiance...
A steampunk laboratory filled with intricate brass instruments and copper piping, steam rising from bubbling alchemical apparatus under warm gaslight...
A cyberpunk street alive with neon advertisements reflecting in rain-soaked asphalt, holographic billboards casting electric blues and magentas...
```

## 🐛 Troubleshooting Dragon Issues 🐛

**Dragon Won't Start?**
- Check Ollama is running: `ollama list`
- Verify Python dependencies: `pip list`
- Ensure port 11434 is free

**Slow Processing?**
- Sparse prompts trigger more retries (this is normal!)
- Consider using more detailed input prompts
- Check your model's performance

**Weird Output?**
- The cleaning system should handle most issues
- Report persistent formatting problems

## 🎭 Advanced Dragon Taming 🎭

### Custom System Prompts
Want to modify the enhancement style? Edit the `system_prompt` variable in `generate_single_prompt()` function.

### Different Word Targets
Adjust the word count range by modifying the validation logic in the retry loop.

### Model Recommendations
- **Fast & Good**: `gemma3:27b`
- **Quality**: `llama3:70b` (if you have the VRAM)
- **Experimental**: Any Ollama model you fancy

## 🤝 Contributing to the Dragon's Hoard 🤝

Found a bug? Want to add features? The dragon welcomes contributors!

1. Fork the repository
2. Create a feature branch
3. Submit a pull request with your enhancements

## 📜 License 📜

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments 🙏

- The magnificent Ollama team for creating the model inference engine
- All the prompt engineers who've shared their wisdom
- Every AI artist who's struggled with sparse prompts (we feel your pain!)

---

**Now go forth and create prompts worthy of dragons! May your images be detailed and your generations swift!** 🐲✨

*Happy prompting, digital alchemists!*