# File: systemSettings.py
import customtkinter as ctk
from utils.dialogs import show_info
from utils.ui_styles import COLORS, get_fonts, PADDING
from navigation import go_to_page, back_to_main

FONTS = get_fonts()


class SystemSettingsPage(ctk.CTkFrame):
    def __init__(self, parent, controller, admin_create_account_page=None, admin_configure_account_page=None):
        super().__init__(parent)
        self.controller = controller
        self.AdminCreateAccountPage = admin_create_account_page
        self.AdminConfigureAccountPage = admin_configure_account_page

        self.configure(
            width=600,
            height=400,
            corner_radius=20,
            fg_color=COLORS["background"]
        )

        # Header
        title = ctk.CTkLabel(
            self,
            text="System Settings",
            font=FONTS["title"]
        )
        title.pack(pady=PADDING["title_y"])

        # Subtitle
        subtitle = ctk.CTkLabel(
            self,
            text="Manage system accounts and preferences",
            font=FONTS["label_font"],
            text_color=COLORS["subtext"]
        )
        subtitle.pack(pady=PADDING["subtitle_y"])

        # Divider
        ctk.CTkFrame(self, height=2, width=500, fg_color=COLORS["divider"]).pack(pady=PADDING["divider_y"])

        # Buttons
        button_width, button_spacing = 250, 15

        ctk.CTkButton(
            self,
            text="Add Account",
            width=button_width,
            command=lambda: go_to_page(self.controller, self.AdminCreateAccountPage)
        ).pack(pady=button_spacing)

        ctk.CTkButton(
            self,
            text="Configure Accounts",
            width=button_width,
            command=lambda: go_to_page(self.controller, self.AdminConfigureAccountPage)
        ).pack(pady=button_spacing)

        ctk.CTkButton(
            self,
            text="Back to Main Menu",
            width=button_width,
            fg_color=COLORS["secondary"],
            hover_color=COLORS["button_hover"],
            command=lambda: back_to_main(self.controller)

        ).pack(pady=button_spacing)
