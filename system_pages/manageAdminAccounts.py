import customtkinter as ctk
from system_pages.account_modifications.createAccounts import CreateAccountsPage
from system_pages.account_modifications.editAccounts import EditAccountsPage
from navigation import back_to_main
from utils.ui_styles import COLORS


class AccountManagerPage(ctk.CTkFrame):
    def __init__(self, parent, controller, main_page_class=None):
        super().__init__(parent)
        self.controller = controller
        self.main_page_class = main_page_class
        self.configure(width=300, height=550, corner_radius=20, fg_color=COLORS["background"])
        self.pack_propagate(False)

        # Title
        ctk.CTkLabel(
            self, text="Admin Account Management",
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(pady=(40, 10))

        # Subtitle
        ctk.CTkLabel(
            self,
            text="Create and manage user accounts for the mobile app.",
            font=ctk.CTkFont(size=14),
            text_color="#00bfff",
            wraplength=260,
            justify="center"
        ).pack(pady=(0, 20))

        # Divider
        ctk.CTkFrame(self, height=2, width=260, fg_color="#2f2f2f").pack(pady=(0, 25))

        # Buttons
        ctk.CTkButton(
            self, text="Create New Account", width=220, height=40,
            font=ctk.CTkFont(size=14),
            command=lambda: controller.show_page(CreateAccountsPage)
        ).pack(pady=10)

        ctk.CTkButton(
            self, text="View / Edit Accounts", width=220, height=40,
            font=ctk.CTkFont(size=14),
            command=lambda: controller.show_page(EditAccountsPage)
        ).pack(pady=10)

        ctk.CTkButton(
            self, text="Back to Main Menu", width=220, height=40,
            font=ctk.CTkFont(size=14),
            fg_color="#34495e", hover_color="#2c3e50",
            command=lambda: back_to_main(self.controller)
        ).pack(pady=(30, 0))
