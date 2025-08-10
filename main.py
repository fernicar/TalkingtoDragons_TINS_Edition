import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QGroupBox, QRadioButton, QComboBox,
    QLabel, QFileDialog, QMessageBox, QScrollArea, QMenuBar, QMenu,
    QSpinBox, QLineEdit, QStatusBar, QStyleFactory
)
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtCore import Qt, Slot, QThread, Signal, QObject

# Import logic and theme
import llm_integration
import theme

class Worker(QObject):
    """
    Worker thread for long-running tasks.
    """
    progress_updated = Signal(str)
    prompt_finished = Signal(str)
    finished = Signal()

    def __init__(self, prompts, model_name, is_chinese, is_enhancement):
        super().__init__()
        self.prompts = prompts
        self.model_name = model_name
        self.is_chinese = is_chinese
        self.is_enhancement = is_enhancement

    @Slot()
    def run(self):
        try:
            for i, prompt in enumerate(self.prompts):
                self.progress_updated.emit(f"Processing prompt {i+1}/{len(self.prompts)}...")

                if self.is_chinese:
                    result, _ = llm_integration.generate_chinese_prompt(prompt, self.model_name, self.is_enhancement)
                else:
                    result, _ = llm_integration.generate_single_prompt(prompt, self.model_name, self.is_enhancement)

                self.prompt_finished.emit(result)
        except Exception as e:
            self.progress_updated.emit(f"An error occurred: {e}")
        finally:
            self.finished.emit()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dragon Diffusion - Talking to Dragons")
        self.setGeometry(100, 100, 1000, 800)
        self.setMinimumSize(900, 700)

        self._create_actions()
        self._create_menu_bar()
        self._create_main_ui()

        # Set default style and populate models
        QApplication.setStyle(QStyleFactory.create("Fusion"))
        self._populate_models()
        self._connect_signals()

    def _connect_signals(self):
        self.enhance_radio.toggled.connect(self._on_mode_change)
        self.load_button.clicked.connect(self._load_prompt_file)
        self.clear_button.clicked.connect(self._clear_all)
        self.save_button.clicked.connect(self._save_output_file)
        self.process_eng_button.clicked.connect(self._process_english)
        self.process_cn_button.clicked.connect(self._process_chinese)

    def _create_actions(self):
        self.quit_action = QAction("&Quit", self)
        self.quit_action.setShortcut(QKeySequence.StandardKey.Quit)
        self.quit_action.triggered.connect(self.close)

    def _create_menu_bar(self):
        menu_bar = self.menuBar()

        # File Menu
        file_menu = menu_bar.addMenu("&File")
        file_menu.addAction(self.quit_action)

        # Theme Menu
        theme_menu = menu_bar.addMenu("&Theme")

        style_menu = theme_menu.addMenu("Style")
        for style in QStyleFactory.keys():
            style_action = QAction(style, self)
            style_action.triggered.connect(self._on_style_selected)
            style_menu.addAction(style_action)

        color_scheme_menu = theme_menu.addMenu("Color Scheme")
        self.auto_scheme_action = QAction("Auto", self, checkable=True)
        self.auto_scheme_action.triggered.connect(lambda: self._on_color_scheme_selected("Auto"))
        self.light_scheme_action = QAction("Light", self, checkable=True)
        self.light_scheme_action.triggered.connect(lambda: self._on_color_scheme_selected("Light"))
        self.dark_scheme_action = QAction("Dark", self, checkable=True)
        self.dark_scheme_action.triggered.connect(lambda: self._on_color_scheme_selected("Dark"))

        color_scheme_menu.addAction(self.auto_scheme_action)
        color_scheme_menu.addAction(self.light_scheme_action)
        color_scheme_menu.addAction(self.dark_scheme_action)

        theme_menu.addSeparator()
        self.dragon_theme_action = QAction("Dragon Diffusion Theme", self)
        self.dragon_theme_action.triggered.connect(self._apply_dragon_theme)
        theme_menu.addAction(self.dragon_theme_action)


    def _create_main_ui(self):
        # Main container widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)

        # --- Title ---
        title_label = QLabel("Dragon Diffusion")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        subtitle_label = QLabel("Talking to Dragons")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("font-size: 14px; font-style: italic;")
        tagline_label = QLabel("Professional Prompt Enhancement Suite")
        tagline_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tagline_label.setStyleSheet("font-size: 10px;")

        main_layout.addWidget(title_label)
        main_layout.addWidget(subtitle_label)
        main_layout.addWidget(tagline_label)

        # --- Mode Selection ---
        mode_group = QGroupBox("Processing Mode")
        mode_layout = QHBoxLayout()
        self.enhance_radio = QRadioButton("Enhance Existing Prompts")
        self.enhance_radio.setChecked(True)
        self.generate_radio = QRadioButton("Generate New Variations")
        mode_layout.addWidget(self.enhance_radio)
        mode_layout.addWidget(self.generate_radio)
        mode_group.setLayout(mode_layout)
        main_layout.addWidget(mode_group)

        # --- Configuration Boxes ---
        self.enhance_box = QGroupBox("Enhancement Mode")
        enhance_layout = QVBoxLayout()
        self.file_label = QLabel("No file loaded")
        self.load_button = QPushButton("Load Prompt File")
        enhance_layout.addWidget(self.file_label)
        enhance_layout.addWidget(self.load_button)
        self.enhance_box.setLayout(enhance_layout)
        main_layout.addWidget(self.enhance_box)

        self.generate_box = QGroupBox("Generation Mode")
        generate_layout = QHBoxLayout()
        theme_label = QLabel("Theme/Style:")
        self.theme_entry = QLineEdit()
        count_label = QLabel("Number of prompts:")
        self.count_spinbox = QSpinBox()
        self.count_spinbox.setRange(1, 1000)
        self.count_spinbox.setValue(50)
        generate_layout.addWidget(theme_label)
        generate_layout.addWidget(self.theme_entry)
        generate_layout.addWidget(count_label)
        generate_layout.addWidget(self.count_spinbox)
        self.generate_box.setLayout(generate_layout)
        main_layout.addWidget(self.generate_box)
        self.generate_box.setVisible(False) # Hidden by default

        self.enhance_radio.toggled.connect(self._on_mode_change)

        # --- Model Selection ---
        model_group = QGroupBox("Model Selection")
        model_layout = QHBoxLayout()
        model_label = QLabel("Ollama Model:")
        self.model_combo = QComboBox()
        model_layout.addWidget(model_label)
        model_layout.addWidget(self.model_combo)
        model_group.setLayout(model_layout)
        main_layout.addWidget(model_group)

        # --- Control Buttons ---
        button_layout = QHBoxLayout()
        self.process_eng_button = QPushButton("Process English Prompts")
        self.process_cn_button = QPushButton("Process Chinese Prompts")
        self.save_button = QPushButton("Save Output")
        self.clear_button = QPushButton("Clear All")
        button_layout.addWidget(self.process_eng_button)
        button_layout.addWidget(self.process_cn_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.clear_button)
        main_layout.addLayout(button_layout)

        # --- Input/Output Areas ---
        io_layout = QHBoxLayout()
        input_group = QGroupBox("Input Prompts")
        input_group_layout = QVBoxLayout()
        self.input_text = QTextEdit()
        input_group_layout.addWidget(self.input_text)
        input_group.setLayout(input_group_layout)

        output_group = QGroupBox("Enhanced Prompts")
        output_group_layout = QVBoxLayout()
        self.output_text = QTextEdit()
        output_group_layout.addWidget(self.output_text)
        output_group.setLayout(output_group_layout)

        io_layout.addWidget(input_group)
        io_layout.addWidget(output_group)
        main_layout.addLayout(io_layout)

        # --- Status Bar ---
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

        # --- Scroll Area ---
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(main_widget)
        self.setCentralWidget(scroll_area)

    def _populate_models(self):
        self.status_bar.showMessage("Fetching Ollama models...")
        try:
            models = llm_integration.fetch_ollama_models()
            self.model_combo.addItems(models)
            self.status_bar.showMessage("Models loaded successfully.", 3000)
        except Exception as e:
            self.status_bar.showMessage(f"Error fetching models: {e}", 5000)
            QMessageBox.critical(self, "Error", f"Could not fetch Ollama models. Make sure Ollama is running.\n\n{e}")

    @Slot()
    def _load_prompt_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Prompt File", "", "Text Files (*.txt);;All Files (*.*)")
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                self.input_text.setPlainText(content)
                num_prompts = len(content.split('\n'))
                self.file_label.setText(f"Loaded: {file_path.split('/')[-1]} ({num_prompts} prompts)")
                self.status_bar.showMessage(f"Loaded {num_prompts} prompts.", 3000)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load file: {e}")

    @Slot()
    def _save_output_file(self):
        content = self.output_text.toPlainText()
        if not content:
            QMessageBox.warning(self, "Warning", "No output to save.")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Save Enhanced Prompts", "", "Text Files (*.txt);;All Files (*.*)")
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                self.status_bar.showMessage(f"Saved to {file_path.split('/')[-1]}", 3000)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file: {e}")

    @Slot()
    def _clear_all(self):
        self.input_text.clear()
        self.output_text.clear()
        self.file_label.setText("No file loaded")
        self.status_bar.showMessage("Cleared all content.", 3000)

    def _get_prompts(self):
        if self.enhance_radio.isChecked():
            input_content = self.input_text.toPlainText().strip()
            if not input_content:
                QMessageBox.warning(self, "Warning", "No input prompts to enhance.")
                return None
            return [line.strip() for line in input_content.split('\n') if line.strip()]
        else: # Generation mode
            theme = self.theme_entry.text().strip()
            if not theme:
                QMessageBox.warning(self, "Warning", "Please enter a theme/style for generation.")
                return None
            count = self.count_spinbox.value()
            return [theme] * count

    @Slot()
    def _process_english(self):
        self._process_prompts(is_chinese=False)

    @Slot()
    def _process_chinese(self):
        self._process_prompts(is_chinese=True)

    def _process_prompts(self, is_chinese):
        prompts = self._get_prompts()
        if not prompts:
            return

        model_name = self.model_combo.currentText()
        if not model_name:
            QMessageBox.warning(self, "Warning", "Please select an Ollama model.")
            return

        is_enhancement = self.enhance_radio.isChecked()
        self.output_text.clear()

        self.thread = QThread()
        self.worker = Worker(prompts, model_name, is_chinese, is_enhancement)
        self.worker.moveToThread(self.thread)

        # Connect signals
        self.worker.progress_updated.connect(self._update_status)
        self.worker.prompt_finished.connect(self._append_result)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self._on_processing_finished)

        self.thread.start()

        self.process_eng_button.setEnabled(False)
        self.process_cn_button.setEnabled(False)
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        self.status_bar.showMessage("Processing...")

    @Slot(str)
    def _update_status(self, message):
        self.status_bar.showMessage(message)

    @Slot(str)
    def _append_result(self, result):
        current_text = self.output_text.toPlainText()
        if current_text:
            self.output_text.setPlainText(current_text + "\n" + result)
        else:
            self.output_text.setPlainText(result)

    @Slot()
    def _on_processing_finished(self):
        self.process_eng_button.setEnabled(True)
        self.process_cn_button.setEnabled(True)
        QApplication.restoreOverrideCursor()
        self.status_bar.showMessage("Completed!", 5000)


    @Slot()
    def _on_mode_change(self):
        is_enhance = self.enhance_radio.isChecked()
        self.enhance_box.setVisible(is_enhance)
        self.generate_box.setVisible(not is_enhance)

    @Slot()
    def _on_style_selected(self):
        action = self.sender()
        style_name = action.text()
        QApplication.setStyle(QStyleFactory.create(style_name))
        self.auto_scheme_action.setChecked(False)
        self.light_scheme_action.setChecked(False)
        self.dark_scheme_action.setChecked(False)

    @Slot()
    def _on_color_scheme_selected(self, scheme):
        if scheme == "Auto":
            QApplication.instance().styleHints().setColorScheme(Qt.ColorScheme.Unknown)
            self.auto_scheme_action.setChecked(True)
            self.light_scheme_action.setChecked(False)
            self.dark_scheme_action.setChecked(False)
        elif scheme == "Light":
            QApplication.instance().styleHints().setColorScheme(Qt.ColorScheme.Light)
            self.auto_scheme_action.setChecked(False)
            self.light_scheme_action.setChecked(True)
            self.dark_scheme_action.setChecked(False)
        elif scheme == "Dark":
            QApplication.instance().styleHints().setColorScheme(Qt.ColorScheme.Dark)
            self.auto_scheme_action.setChecked(False)
            self.light_scheme_action.setChecked(False)
            self.dark_scheme_action.setChecked(True)

        # Reset to remove custom QSS
        QApplication.instance().setStyleSheet("")


    @Slot()
    def _apply_dragon_theme(self):
        self.auto_scheme_action.setChecked(False)
        self.light_scheme_action.setChecked(False)
        self.dark_scheme_action.setChecked(False)
        QApplication.instance().setStyleSheet(theme.DRAGON_THEME_QSS)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
