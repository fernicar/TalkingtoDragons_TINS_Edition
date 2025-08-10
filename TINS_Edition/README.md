# TINS Documentation: Dragon Diffusion GUI Refactor

This document details the architecture, design, and implementation plan for refactoring the "Dragon Diffusion" application to a modern PySide6 GUI, following the principles of "There Is No Source" (TINS).

## 1. Project Overview

**Dragon Diffusion** is a specialized tool for prompt engineering. It helps artists and designers enhance and generate creative prompts for text-to-image models, specifically the "Flux Dev" model. It provides two core functionalities:

1.  **Enhancement**: Takes a list of basic prompts and uses a Large Language Model (LLM) to enrich them with artistic detail.
2.  **Generation**: Creates a batch of unique prompt variations based on a central theme or style.

The application interacts with a locally-hosted Ollama server to leverage its LLM capabilities and supports both English and Chinese languages. This project's goal is to replace the original `tkinter` GUI with a more robust, modern, and maintainable PySide6 interface.

## 2. TINS Motivation

This refactoring project is being conducted with the **TINS methodology** as a guiding principle. The primary goal is not just to produce a working application, but to produce a set of clear, detailed, and well-structured documents (`README.md`, `GUI_progress.md`) that could theoretically be used by an AI agent to generate the application source code from scratch.

By focusing on documenting the *what* and the *why*, we create a blueprint that is decoupled from a single implementation. This `TINS_Edition` directory serves as the "source of truth" for the application's design and logic.

## 3. Application Architecture

The new application will follow a modular, multi-file structure to ensure a clean separation of concerns between the user interface (View), business logic (Model), and utility functions.

-   **`main.py` (View/Controller)**: This will be the main entry point of the application. It is responsible for:
    -   Creating and displaying the `QMainWindow` and all GUI widgets (buttons, text boxes, etc.).
    -   Managing the layout and overall presentation.
    -   Handling all user interactions (e.g., button clicks, text input) through signals and slots.
    -   Delegating business logic tasks to the `llm_integration` module.

-   **`llm_integration.py` (Model)**: This module will contain all the core business logic and handle all communication with the external Ollama API. Its responsibilities include:
    -   Fetching the list of available Ollama models.
    -   Constructing the correct system and user prompts for enhancement and generation tasks.
    -   Making HTTP requests to the Ollama `/api/generate` endpoint.
    -   Processing the streaming response from the API.
    -   Running in a separate `QThread` to avoid blocking the GUI during long-running API calls.

-   **`utils.py` (Utilities)**: A collection of helper functions that can be used across the application. Its initial responsibility will be:
    -   Housing the `clean_prompt_output` function, which sanitizes the raw text received from the LLM.

-   **`theme.py` (Styling)**: This file will contain the QSS (Qt Style Sheets) for the application's custom "Dragon Diffusion" theme, allowing for easy reuse and modification of the visual style.

## 4. Component Relationships & Data Flow

The components are designed to be loosely coupled, communicating primarily through function calls and Qt's signal/slot mechanism.

**Typical Data Flow (Enhancement Mode):**

1.  **User Action**: The user clicks the "Load Prompt File" button in `main.py`.
2.  **GUI Event**: A `clicked` signal is emitted.
3.  **Controller Logic**: A slot in `main.py` opens a `QFileDialog`, reads the selected file's content, and displays it in the input `QTextEdit`.
4.  **User Action**: The user clicks the "Process Prompts" button.
5.  **GUI Event**: A `clicked` signal is emitted.
6.  **Controller Logic**: A slot in `main.py` retrieves the prompts from the input `QTextEdit` and the selected model from the `QComboBox`.
7.  **Business Logic Delegation**: The controller calls a function in `llm_integration.py` (e.g., `start_processing`), passing the prompts and model name.
8.  **Asynchronous Execution**: `llm_integration.py` starts a `QThread` to handle the API calls without freezing the GUI.
9.  **API Interaction**: The thread sends requests to the Ollama API for each prompt.
10. **Feedback Loop**: As each prompt is processed, the thread emits signals back to the main thread with the result and status updates.
11. **GUI Update**: Slots in `main.py` receive these signals and update the output `QTextEdit` and the status label in real-time.

## 5. Design Rationale

-   **PySide6**: Chosen over `tkinter` for its modern object-oriented API, extensive widget library, powerful styling system (QSS), and robust signal/slot mechanism, which is ideal for separating business logic from the UI.
-   **Separation of Concerns**: By splitting the code into dedicated modules, the application becomes easier to understand, debug, and extend. Changes to the UI (`main.py`) can be made with minimal impact on the backend logic (`llm_integration.py`), and vice-versa.
-   **Asynchronous Operations**: Using `QThread` for network requests is critical for a good user experience. It ensures the application remains responsive and doesn't "freeze" while waiting for the LLM to return a response.
-   **Dynamic Theming**: The inclusion of a theme selection menu (featuring styles like "Fusion" and a custom "Dragon" theme) provides user flexibility and demonstrates the power of QSS for creating adaptable and visually appealing interfaces.
