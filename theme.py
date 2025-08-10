# Welsh Dragon Colour Scheme
BG_BLACK = "#0d0d0d"
BG_CHARCOAL = "#1a1a1a"
SCARLET_RED = "#dc143c"
RICH_GOLD = "#ffd700"
DARK_GOLD = "#b8860b"
TEXT_WHITE = "#ffffff"
TEXT_SILVER = "#c0c0c0"

# Custom QSS Stylesheet for the "Dragon Diffusion" theme
# This will be applied on top of a base style like "Fusion"
DRAGON_THEME_QSS = f"""
    QMainWindow, QDialog {{
        background-color: {BG_BLACK};
    }}
    QGroupBox {{
        background-color: {BG_BLACK};
        color: {RICH_GOLD};
        border: 2px solid {RICH_GOLD};
        border-radius: 5px;
        margin-top: 1ex; /* leave space at the top for the title */
        font-weight: bold;
    }}
    QGroupBox::title {{
        subcontrol-origin: margin;
        subcontrol-position: top center; /* position at the top center */
        padding: 0 3px;
        background-color: {BG_BLACK};
    }}
    QLabel {{
        color: {TEXT_WHITE};
        background-color: transparent;
    }}
    QRadioButton, QCheckBox {{
        color: {TEXT_WHITE};
    }}
    QRadioButton::indicator::unchecked {{
        border: 1px solid {RICH_GOLD};
        border-radius: 6px;
        background-color: {BG_CHARCOAL};
        width: 12px;
        height: 12px;
    }}
    QRadioButton::indicator::checked {{
        border: 1px solid {RICH_GOLD};
        border-radius: 6px;
        background-color: {SCARLET_RED};
        width: 12px;
        height: 12px;
    }}
    QPushButton {{
        background-color: {SCARLET_RED};
        color: {TEXT_WHITE};
        border: 2px solid {DARK_GOLD};
        padding: 5px 15px;
        border-radius: 5px;
        font-weight: bold;
    }}
    QPushButton:hover {{
        background-color: {DARK_GOLD};
    }}
    QPushButton:pressed {{
        background-color: #a07000;
    }}
    QTextEdit, QLineEdit, QSpinBox, QComboBox {{
        background-color: {BG_CHARCOAL};
        color: {TEXT_WHITE};
        border: 1px solid {RICH_GOLD};
        border-radius: 3px;
        padding: 2px;
    }}
    QComboBox::drop-down {{
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 15px;
        border-left-width: 1px;
        border-left-color: {RICH_GOLD};
        border-left-style: solid;
        border-top-right-radius: 3px;
        border-bottom-right-radius: 3px;
    }}
    QComboBox::down-arrow {{
        image: url(placeholder.png); /* A real app would use a resource file */
    }}
    QMenuBar {{
        background-color: {BG_BLACK};
        color: {TEXT_WHITE};
    }}
    QMenuBar::item:selected {{
        background-color: {BG_CHARCOAL};
    }}
    QMenu {{
        background-color: {BG_CHARCOAL};
        color: {TEXT_WHITE};
        border: 1px solid {RICH_GOLD};
    }}
    QMenu::item:selected {{
        background-color: {SCARLET_RED};
    }}
    QStatusBar {{
        color: {RICH_GOLD};
    }}
"""
