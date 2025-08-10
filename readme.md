# 🐲 Dragon Diffusion - Talking to Dragons 🐲

**Professional Prompt Enhancement Suite**

Welcome, digital alchemists and prompt enchanters! Ever felt like your image generation prompts were more like whimpers than roars? Fear not! **Dragon Diffusion - Talking to Dragons** is here to transform your measly prompt scraps into magnificent, fire-breathing descriptions that'll make even the most stubborn AI dragons sit up and pay attention! ✨

This mystical application harnesses the power of local Ollama models to take your basic prompts and enhance them into rich, detailed masterpieces worthy of the finest image generation spells. Say goodbye to bland "cat on beach" prompts and hello to epic 250-300 word sagas!

## 🌟 What Does This Dragon Do? 🌟

Transform your prompts from this:
```
A bioluminescent mushroom forest inhabited by miniature clockwork dragons
```

Into THIS legendary tome:
```
A breathtaking ultra-wide panoramic vista of a bioluminescent fungal forest sprawling across a fractured amethyst mesa, colossal crystalline structures resembling gothic spires piercing a swirling nebula sky filled with cosmic dust and ethereal light, six-legged insectoid creatures with intricately detailed chitinous exoskeletons delicately tending glowing gardens of pulsating fungi and crystalline flora, dramatic volumetric lighting casting long, dancing shadows and illuminating iridescent spores, hyperdetailed textures of fungal gills, crystalline facets, and insectoid anatomy, art by Roger Dean and Zdzisław Beksiński with subtle influences of H.R. Giger's biomechanical aesthetic...
```

## 🎭 Magical Processing Modes 🎭

### 🔮 Enhancement Mode
Feed it your existing prompt lists and watch them grow into detailed epics with professional artistic terminology, camera specifications, and lighting descriptions.

### ⚡ Generation Mode  
Give it a theme ("Lovecraftian horror with tentacles and dread") and it'll spawn fresh prompt variations from the void.

### 🉐 Chinese Token Efficiency
**The secret weapon:** Simplified Chinese prompts pack 30-40% more information into the same token budget! Generate ultra-dense prompts that squeeze maximum detail into token-limited models.

**English:** 300 words maximum
**Chinese:** Equivalent of 400+ words of information density

Perfect for multilingual models that understand Chinese but you don't need to speak it - just exploit the linguistic efficiency!

---

## 🚀 **New PySide6 GUI (Under Development)** 🚀

This application is currently undergoing a significant architectural refactor. The original `tkinter`-based GUI is being replaced with a modern, robust, and maintainable interface built with **PySide6 (version 6.9.1)**. This section outlines the new architecture.

### Architectural Principles

The new design is guided by the principle of **Separation of Concerns**, moving away from a single-file script to a modular structure that is easier to manage and extend. It loosely follows a Model-View-Controller (MVC) pattern:

-   **`main.py` (View/Controller)**: The main application entry point, responsible for creating and managing all GUI elements using PySide6 widgets. It handles user interactions and orchestrates calls to the business logic.
-   **`llm_integration.py` (Model)**: Contains the core business logic. All interactions with the Ollama API—such as fetching models, constructing prompts, and processing requests—are encapsulated here.
-   **`utils.py` (Utilities)**: A collection of shared helper functions, such as the text-cleaning logic for the LLM output.
-   **`theme.py` (Styling)**: Holds the custom QSS (Qt Style Sheets) for the "Dragon Diffusion" theme.

### Key PySide6 Features

The new implementation leverages powerful features of the Qt6 framework to create a responsive and feature-rich user experience:

-   **Widget Hierarchy & Layouts**: The UI is built with a clear hierarchy of standard widgets (`QMainWindow`, `QGroupBox`, `QTextEdit`, `QComboBox`, etc.) and organized using flexible layout managers (`QVBoxLayout`, `QHBoxLayout`) to ensure the interface is clean and scales correctly.

-   **Signals and Slots**: We are using Qt's core communication mechanism to decouple components. For example, a button's `clicked` signal is connected to a `@Slot` in the controller, which then calls the business logic. This creates a clean, event-driven architecture.

-   **Asynchronous Operations with `QThread`**: All network requests to the Ollama API will be executed in a background thread (`QThread`). This is crucial for ensuring the GUI remains responsive and does not "freeze" while waiting for the LLM to generate a response. The thread will use signals to send data and progress updates back to the main UI thread safely.

-   **Dynamic Theming Engine**: The new GUI features a flexible theming system:
    -   **`QStyleFactory`**: Users can switch between native-looking application styles like "Fusion", "Windows", and "macOS". "Fusion" is used as the default for a consistent cross-platform look.
    -   **Color Schemes**: Full support for light and dark modes by manipulating the `Qt.ColorScheme`.
    -   **Custom QSS**: The original "Welsh Dragon" theme is implemented as a custom stylesheet (`.qss`) that can be applied on top of any style, demonstrating the full power of Qt's styling capabilities.

-   **Modern Idioms**: The new codebase adheres to modern PySide6 best practices, including the use of **scoped enums** (e.g., `Qt.AlignmentFlag.AlignHCenter`) for improved readability and type safety, and Pythonic decorators (`@Slot`, `@Property`) for defining Qt behavior.

---

## 🧙‍♂️ Prerequisites - Gathering Your Magical Components 🧙‍♀️

### 1. Ollama - The Dragon's Brain 🧠
This application speaks directly to local Ollama models:

- Download from [Ollama's official lair](https://ollama.ai/)
- Install a model (we recommend `gemma3:27b` for best results)
- Ensure it's running on `http://localhost:11434`

Test your setup:
```bash
ollama list
```

### 2. Python Environment 🐍
Create a virtual environment:

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
   git clone https://github.com/yourusername/dragon-diffusion-talking-to-dragons.git
   cd dragon-diffusion-talking-to-dragons
   ```

2. **Install the Mystical Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Unleash the Dragon:**
   ```bash
   python main.py
   ```

The new, modern PySide6 GUI will materialize, ready to transform your prompts with enhanced stability and features!

## 🎯 How to Wield This Magical Tool 🎯

### Enhancement Mode (Transform Existing Prompts)
1. **Load Your Prompt Scroll**: Click "Load Prompt File" and select your `.txt` file
   - **CRITICAL**: One prompt per line! No empty lines, just pure prompt goodness
   
2. **Choose Your Processing Language**:
   - **"Process English Prompts"**: Traditional detailed enhancement
   - **"Process Chinese"**: Token-efficient Chinese output for maximum density

3. **Select Your Model**: Choose your preferred Ollama model

4. **Process the Magic**: Watch as each line transforms into enhanced masterpieces

5. **Save Your Enhanced Tome**: Click "Save Output" to preserve your enhanced prompts

### Generation Mode (Create New Prompts)
1. **Select Generation Mode**: Choose "Generate New Variations"

2. **Describe Your Vision**: Enter themes like:
   - "Cyberpunk cityscapes with neon and rain"
   - "Lovecraftian horror with tentacles and cosmic dread" 
   - "Steampunk airships in cloudy skies"

3. **Set Your Quantity**: Default is 50 prompts (adjustable)

4. **Choose Language Output**: English for standard models, Chinese for token efficiency

5. **Let the Dragon Create**: Process and watch new prompts materialise

## 🔗 ComfyUI Integration - The Complete Pipeline 🔗

### Zenkai V5 Node Integration
For seamless ComfyUI workflow integration, use Drift's DJZ-Nodes:

**Repository:** [MushroomFleet/DJZ-Nodes](https://github.com/MushroomFleet/DJZ-Nodes)

**Setup Process:**
1. **Install DJZ-Nodes** in your ComfyUI custom nodes
2. **Save your enhanced prompts** from Dragon Diffusion
3. **Place text files** in: `ComfyUI\custom_nodes\djz-nodes\prompts`
4. **Use Zenkai V5 node** in your ComfyUI workflow
5. **Automated cycling** through your enhanced prompts

**Complete Production Pipeline:**
```
Dragon Diffusion → Enhanced Prompts → ComfyUI Folder → Zenkai V5 → Automated Generation
```

No manual copy/paste needed - pure professional workflow automation!

## ⚠️ Dragon Warnings & Wisdom ⚠️

- **Sparse Input = Longer Processing**: Basic prompts trigger retry logic as the system works to reach word targets
- **Detailed Input = Lightning Fast**: Well-developed prompts process quickly
- **One Prompt Per Line**: The dragon demands this format - no exceptions!
- **Clean Output Guaranteed**: Automatic stripping of LLM artifacts and unwanted formatting
- **Cross-Language Magic**: English→Chinese creates ultra-dense prompts, Chinese→English expands concepts

## 🔧 Technical Sorcery 🔧

### The Enhancement Spell
Each prompt undergoes magical transformation:
1. **Flux-Optimised System Prompts**: Specialised for image generation models
2. **Word/Character Count Validation**: Ensures optimal prompt length
3. **Advanced Cleaning**: Removes thinking blocks, XML tags, and meta-commentary
4. **Language-Specific Processing**: Different strategies for English vs Chinese
5. **Retry Logic**: Smart continuation and graceful fallbacks

### Model Recommendations
- **Best Overall**: `gemma3:27b` - Clean output, reliable, efficient
- **Quality Beast**: `llama3:70b` (if you have the VRAM)
- **Avoid**: Polaris models (thinking bleed issues)

### Language Strategy Guide
**English Processing:**
- Rich artistic terminology
- Technical camera specifications
- 250-300 word sweet spot
- Professional art direction language

**Chinese Processing:**
- Maximum information density
- 150-200 character targets
- Token-efficient descriptions
- Semantic richness over length

## 📁 File Formats 📁

**Input File Format** (one prompt per line):
```
A magical forest with glowing mushrooms
A steampunk laboratory with brass instruments
A cyberpunk street with neon advertisements
```

**English Output Format**:
```
A magical forest bathed in ethereal twilight, where bioluminescent mushrooms cast prismatic glows across moss-covered ground, their caps shimmering with otherworldly radiance, dramatic volumetric lighting piercing through ancient oak canopies, shot with 85mm lens at f/1.8, octane render, 16k resolution...

A steampunk laboratory filled with intricate brass instruments and copper piping, steam rising from bubbling alchemical apparatus under warm gaslight, hyperdetailed textures of polished metal and leather, wide-angle perspective, cinematic composition, art by H.R. Giger and Jules Verne...
```

**Chinese Output Format**:
```
超现实主义魔法森林，生物发光的蘑菇在苔藓覆盖的地面上投射出棱镜般的光芒，帽状结构闪烁着超凡脱俗的光辉，戏剧性的体积光穿透古老橡树的树冠，85mm镜头f/1.8拍摄，octane渲染，16k分辨率...

蒸汽朋克实验室，充满复杂的黄铜仪器和铜管，蒸汽从温暖煤气灯下冒泡的炼金装置中升起，抛光金属和皮革的超细致纹理，广角透视，电影级构图，H.R. Giger和儒勒·凡尔纳风格...
```

## 🐛 Troubleshooting Dragon Issues 🐛

**Dragon Won't Start?**
- Check Ollama is running: `ollama list`
- Verify Python dependencies: `pip list`
- Ensure port 11434 is free

**Slow Processing?**
- Sparse prompts trigger more retries (normal behaviour!)
- Use more detailed input for faster processing
- Check model performance

**Truncated Chinese Output?**
- Normal for token-dense processing
- Enhanced cleaning handles most issues
- Chinese efficiency sometimes hits limits

**UI Layout Issues?**
- Text areas should resize properly
- Check window size and scaling
- Grid layout self-adjusts

## 🎭 Advanced Dragon Taming 🎭

### Custom System Prompts
Modify enhancement styles by editing system prompts in the respective language functions.

### Token Efficiency Tuning
Adjust character/word count targets in the validation logic for different density requirements.

### Cross-Language Workflows
Experiment with English→Chinese→English chains for unique prompt variations.

## 🤝 Contributing to the Dragon's Hoard 🤝

Found a bug? Want to add features? The dragon welcomes contributors!

1. Fork the repository
2. Create a feature branch  
3. Submit a pull request with your enhancements

## 🏴󠁧󠁢󠁷󠁬󠁳󠁿 Welsh Dragon Aesthetics 🏴󠁧󠁢󠁷󠁬󠁳󠁿

The UI features professional Dragon Diffusion branding with Welsh dragon-inspired colours:
- **Deep black** backgrounds for sophistication
- **Scarlet red** primary actions (Welsh dragon red)
- **Rich gold** accents and highlights
- **Professional typography** and spacing
- **Corporate identity** integration

## 📜 License 📜

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments 🙏

- The magnificent Ollama team for local model inference
- Drift Johnson for DJZ-Nodes and ComfyUI integration
- The prompt engineering community sharing wisdom
- Every AI artist who's battled with sparse prompts
- The discovery of Chinese token density efficiency

---

**Now go forth and create prompts worthy of dragons! May your tokens be dense and your generations swift!** 🐲✨

*Happy prompting, digital alchemists!*