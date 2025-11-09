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
        self.configure(width=600, height=400, corner_radius=20, fg_color=COLORS["background"])

        ctk.CTkLabel(self, text="Admin Account Management", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(30, 5))
        ctk.CTkLabel(
            self,
            text="Create and manage user accounts for the mobile app.",
            font=ctk.CTkFont(size=15),
            text_color="#00bfff"
        ).pack(pady=(0, 20))

        ctk.CTkFrame(self, height=2, width=500, fg_color="#2f2f2f").pack(pady=(0, 20))

        ctk.CTkButton(
            self, text="Create New Account", width=250,
            command=lambda: controller.show_page(CreateAccountsPage)
        ).pack(pady=10)

        ctk.CTkButton(
            self, text="View / Edit Accounts", width=250,
            command=lambda: controller.show_page(EditAccountsPage)
        ).pack(pady=10)

        ctk.CTkButton(
            self, text="Back to Main Menu", width=250,
            fg_color="#34495e", hover_color="#2c3e50",
            command=lambda: back_to_main(self.controller)
        ).pack(pady=20)

    