# PySide6 GUI Refactor Plan for Dragon Diffusion

This plan outlines the tasks required to refactor the `tkinter`-based "Talking to Dragons" application into a modern PySide6 GUI.

## I. Project Foundation & Structure

- [ ] **Dependency Management**: Create a `requirements.txt` file with `PySide6==6.9.1` and `requests`.
- [ ] **Modularization**: Create the initial file structure:
    - [ ] `main.py`: Main application entry point, will contain the `QMainWindow` and view logic.
    - [ ] `llm_integration.py`: For all Ollama API interaction logic (fetching models, generating prompts).
    - [ ] `utils.py`: For helper functions, starting with `clean_prompt_output`.
    - [ ] `theme.py`: To store the application's QSS stylesheet for the "Dragon Diffusion" theme.

## II. Main Application Window (`QMainWindow`)

- [ ] **Window Setup**: Create the main window, set the title to "Dragon Diffusion - Talking to Dragons", and define a reasonable default and minimum size.
- [ ] **Central Widget**: Set up a `QScrollArea` as the central widget to ensure the entire UI is scrollable on smaller screens.
- [ ] **Branding**:
    - [ ] Add `QLabel` for the main title ("Dragon Diffusion").
    - [ ] Add `QLabel` for the subtitle ("Talking to Dragons").
    - [ ] Add `QLabel` for the tagline ("Professional Prompt Enhancement Suite").
- [ ] **Layout**: Use `QVBoxLayout` to structure the main sections of the application vertically.

## III. User Input & Configuration Widgets

- [ ] **Processing Mode**:
    - [ ] Create a `QGroupBox` titled "Processing Mode".
    - [ ] Add two `QRadioButton`s: "Enhance Existing Prompts" and "Generate New Variations".
    - [ ] Implement logic to show/hide the correct configuration box based on which radio button is selected.
- [ ] **Enhancement Mode Box (`QGroupBox`)**:
    - [ ] Add a `QLabel` to display the loaded prompt filename ("No file loaded").
    - [ ] Add a `QPushButton` ("Load Prompt File") that opens a `QFileDialog` to select a `.txt` file.
- [ ] **Generation Mode Box (`QGroupBox`)**:
    - [ ] Add a `QLabel` and `QLineEdit` for the "Theme/Style".
    - [ ] Add a `QLabel` and `QSpinBox` for the "Number of prompts".
- [ ] **Model Selection**:
    - [ ] Create a `QGroupBox` titled "Model Selection".
    - [ ] Add a `QLabel` for "Ollama Model:".
    - [ ] Add a `QComboBox` to list and select the available Ollama models.
    - [ ] Implement the `fetch_ollama_models` function in `llm_integration.py` and call it on startup to populate the combo box.

## IV. Core Functionality & Control

- [ ] **Control Buttons**:
    - [ ] Create a `QHBoxLayout` to hold the main action buttons.
    - [ ] Add a `QPushButton` for "Process English Prompts".
    - [ ] Add a `QPushButton` for "Process Chinese Prompts".
    - [ ] Add a `QPushButton` for "Save Output".
    - [ ] Add a `QPushButton` for "Clear All".
- [ ] **Input/Output Text Areas**:
    - [ ] Create a `QHBoxLayout` to place the input and output areas side-by-side.
    - [ ] **Input**: Create a `QGroupBox` ("Input Prompts") containing a `QTextEdit`.
    - [ ] **Output**: Create a `QGroupBox` ("Enhanced Prompts") containing a `QTextEdit`.
- [ ] **Status Bar**:
    - [ ] Create a `QGroupBox` ("Status") containing a `QLabel` to display status updates.

## V. Business Logic & Integration

- [ ] **Signal/Slot Connections**:
    - [ ] Connect the "Load Prompt File" button's `clicked` signal to a slot that reads the file and populates the input `QTextEdit`.
    - [ ] Connect the "Process..." buttons' `clicked` signals to slots that trigger the appropriate generation logic in `llm_integration.py`.
    - [ ] Connect the "Save Output" button's `clicked` signal to a slot that opens a `QFileDialog` to save the content of the output `QTextEdit`.
    - [ ] Connect the "Clear All" button's `clicked` signal to a slot that clears the input/output text areas and resets the file label.
- [ ] **Logic Refactoring**:
    - [ ] Move `generate_single_prompt` and `generate_chinese_prompt` into `llm_integration.py`.
    - [ ] Modify the processing loops (`process_prompts`, `process_chinese_prompts`) to be non-blocking or run in a separate thread (`QThread`) to keep the GUI responsive. They should emit signals to update the UI with progress and results.
- [ ] **Status Updates**: Implement a mechanism (e.g., a custom signal) to update the status label from the business logic threads.

## VI. Theme Selection Menu

- [ ] **Menu Bar**: Add a `QMenuBar` to the `QMainWindow`.
- [ ] **Theme Menu**: Create a "Theme" menu in the menu bar.
- [ ] **Style Options**:
    - [ ] Add actions to the menu to switch between `QStyleFactory` themes (e.g., "Fusion", "Windows", "macOS").
    - [ ] Set "Fusion" as the default style.
- [ ] **Color Scheme**:
    - [ ] Add a submenu for color schemes, including an "Auto" option that uses system colors.
    - [ ] Add an option for the custom "Dragon Diffusion" theme.
- [ ] **Custom Theme Logic**:
    - [ ] The "Dragon Diffusion" theme will load a custom QSS stylesheet from `theme.py`.
    - [ ] All other themes will use the standard PySide6 styling.

## VII. Finalization

- [ ] **Final Review**: Ensure all widgets are styled correctly, themes apply properly, layouts are balanced, and the application is responsive.
- [ ] **README Update**: Update the root `README.md` with instructions on how to install and run the new PySide6 application.
