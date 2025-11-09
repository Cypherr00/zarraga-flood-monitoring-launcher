# File: utils/ui_styles.py

import customtkinter as ctk

# === Colors ===
PRIMARY_COLOR = "#00bfff"        # Accent blue
BACKGROUND_COLOR = "#0d0d0d"     # Main dark background
SECONDARY_BG = "#1a1a1a"         # Frame color
TEXT_COLOR = "#ffffff"
SUBTEXT_COLOR = "#7f8c8d"
DANGER_COLOR = "#c0392b"
BUTTON_HOVER_DANGER = "#a93226"
BUTTON_NORMAL = "#34495e"
BUTTON_HOVER = "#2c3e50"

# === Fonts ===
def title_font(size=24):
    """Return a bold CTkFont for titles."""
    try:
        return ctk.CTkFont(size=size, weight="bold")
    except RuntimeError:
        # If called too early, return None (safe fallback)
        return None

def label_font(size=16):
    """Return a normal CTkFont for general labels."""
    try:
        return ctk.CTkFont(size=size)
    except RuntimeError:
        return None

def small_font(size=12):
    """Return a smaller CTkFont for status or sublabels."""
    try:
        return ctk.CTkFont(size=size)
    except RuntimeError:
        return None

# === Buttons ===
def styled_button(master, text, command, color=BUTTON_NORMAL,
                  hover_color=BUTTON_HOVER, width=250):
    """Return a consistently styled CTkButton."""
    return ctk.CTkButton(
        master,
        text=text,
        width=width,
        fg_color=color,
        hover_color=hover_color,
        font=label_font(16) or ("Arial", 14),
        command=command
    )

# === Color map ===
COLORS = {
    "accent": PRIMARY_COLOR,
    "background": BACKGROUND_COLOR,
    "secondary": SECONDARY_BG,
    "text": TEXT_COLOR,
    "subtext": SUBTEXT_COLOR,
    "danger": DANGER_COLOR,
    "danger_hover": BUTTON_HOVER_DANGER,
    "button": BUTTON_NORMAL,
    "button_hover": BUTTON_HOVER,
    "divider": "#2f2f2f",
}

# === Font map (lazy creation) ===
def get_fonts():
    return {
        "title": title_font(24),
        "water_level": label_font(16),
        "label_font": label_font(16),
    }

# === Padding ===
PADDING = {
    "title_y": (30, 5),
    "subtitle_y": (0, 20),
    "divider_y": (10, 20),
}
