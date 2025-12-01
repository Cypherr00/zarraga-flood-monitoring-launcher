import customtkinter as ctk

# === Colors ===
PRIMARY_COLOR = "#0078ff"        # Accent blue (bright blue)
BACKGROUND_COLOR = "#f2f6fc"     # Main light background
SECONDARY_BG = "#e3edf8"         # Light frame / panel background
TEXT_COLOR = "#1f4e79"           # Dark blue text
SUBTEXT_COLOR = "#6f7b86"        # Soft grey subtext
DANGER_COLOR = "#d9534f"         # Light-theme friendly danger red
BUTTON_HOVER_DANGER = "#c9302c"

# Neutral buttons for light theme
BUTTON_NORMAL = "#1f6fbf"        # Blue button background
BUTTON_HOVER = "#155c99"         # Darker blue hover

# Divider
DIVIDER_COLOR = "#cce0ff"        # Light blue divider / borders

# === Fonts ===
def title_font(size=24):
    """Return a bold CTkFont for titles."""
    try:
        return ctk.CTkFont(size=size, weight="bold")
    except RuntimeError:
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
        text_color=TEXT_COLOR,
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
    "divider": DIVIDER_COLOR,
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
