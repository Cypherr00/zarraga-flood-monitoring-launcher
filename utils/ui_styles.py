import customtkinter as ctk

# ============================================================
#   BASE COLORS — PROFESSIONAL LIGHT THEME WITH BLUE ACCENTS
# ============================================================

PRIMARY_COLOR = "#0074e6"        # Slightly darker blue for professionalism
BACKGROUND_COLOR = "#f9f9f9"     # Clean light-gray white background
SECONDARY_BG = "#ffffff"         # White cards/panels (modern contrast)
TEXT_COLOR = "#1e1e1e"           # Deep neutral black for readability
SUBTEXT_COLOR = "#4a4a4a"        # Soft but readable grey for descriptions
DANGER_COLOR = "#c0392b"         # Professional red tone
BUTTON_HOVER_DANGER = "#a93226"  # Slightly darker hover red

# Button variations suitable for a light environment
BUTTON_NORMAL = "#e6e6e6"        # Soft neutral grey button
BUTTON_HOVER = "#d0d0d0"         # Darker hover for visual feedback

# Divider line for structure separation
DIVIDER_COLOR = "#d5d5d5"        # Muted grey for modern separation lines

# ============================================================
#   FONTS — KEEPING THEM CONSISTENT AND READABLE
# ============================================================

def title_font(size=24):
    """Bold title font used for page headers."""
    try:
        return ctk.CTkFont(size=size, weight="bold")
    except RuntimeError:
        return None

def label_font(size=16):
    """Standard font for labels and body text."""
    try:
        return ctk.CTkFont(size=size)
    except RuntimeError:
        return None

def small_font(size=12):
    """Smaller font for hints, sublabels, or small UI elements."""
    try:
        return ctk.CTkFont(size=size)
    except RuntimeError:
        return None

# ============================================================
#   STANDARDIZED BUTTON
# ============================================================

def styled_button(master, text, command, color=BUTTON_NORMAL,
                  hover_color=BUTTON_HOVER, width=250):
    """Return a consistent light-theme compatible CTkButton."""
    return ctk.CTkButton(
        master,
        text=text,
        width=width,
        fg_color=color,
        hover_color=hover_color,
        font=label_font(16) or ("Arial", 14),
        text_color=TEXT_COLOR,
        corner_radius=8,
        command=command
    )

# ============================================================
#   COLOR MAP (DO NOT RENAME KEYS)
# ============================================================

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

# ============================================================
#   FONT MAP
# ============================================================

def get_fonts():
    return {
        "title": title_font(24),
        "water_level": label_font(16),
        "label_font": label_font(16),
    }

# ============================================================
#   PADDING CONSTANTS — KEPT SIMPLE & UNIVERSAL
# ============================================================

PADDING = {
    "title_y": (25, 5),
    "subtitle_y": (0, 18),
    "divider_y": (12, 18),
}
