# File: system_pages/adminConfigureAccounts.py

import customtkinter as ctk
from utils.dialogs import show_info, show_error, ask_confirm
from utils.ui_styles import COLORS, get_fonts
import re

FONTS = get_fonts()


class adminConfigureAccountsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.supabase = controller.supabase
        self.configure(fg_color=COLORS["background"])

        # === Title Section ===
        ctk.CTkLabel(
            self,
            text="Configure Account",
            font=FONTS["title"],
            text_color=COLORS["accent"],
        ).pack(pady=(30, 10))

        ctk.CTkLabel(
            self,
            text="Update your username or password.",
            font=FONTS["label_font"],
            text_color=COLORS["subtext"],
        ).pack(pady=(0, 20))

        # === Form Frame ===
        form = ctk.CTkFrame(self, fg_color=COLORS["secondary"], corner_radius=12)
        form.pack(padx=40, pady=10, fill="x")

        # New Username
        ctk.CTkLabel(form, text="New Username:", text_color=COLORS["text"]).pack(anchor="w", padx=20, pady=(15, 0))
        self.entry_new_username = ctk.CTkEntry(form, width=320)
        self.entry_new_username.pack(padx=20, pady=(0, 10))

        # New Password
        ctk.CTkLabel(form, text="New Password:", text_color=COLORS["text"]).pack(anchor="w", padx=20, pady=(5, 0))
        self.entry_new_pass = ctk.CTkEntry(form, width=320, show="•")
        self.entry_new_pass.pack(padx=20, pady=(0, 10))

        # Confirm Password
        ctk.CTkLabel(form, text="Confirm Password:", text_color=COLORS["text"]).pack(anchor="w", padx=20, pady=(5, 0))
        self.entry_confirm_pass = ctk.CTkEntry(form, width=320, show="•")
        self.entry_confirm_pass.pack(padx=20, pady=(0, 20))

        # === Buttons ===
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=(10, 30))

        ctk.CTkButton(
            btn_frame,
            text="Update Account",
            fg_color=COLORS["accent"],
            hover_color=COLORS["button_hover"],
            command=self.show_confirm_password_popup,
            width=200,
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            btn_frame,
            text="Back",
            fg_color=COLORS["button"],
            hover_color=COLORS["button_hover"],
            command=lambda: controller.show_page("SystemSettingsPage"),
            width=120,
        ).pack(side="left", padx=10)

    # === Popup for password confirmation ===
    def show_confirm_password_popup(self):
        new_username = self.entry_new_username.get().strip()
        new_pass = self.entry_new_pass.get().strip()
        confirm_pass = self.entry_confirm_pass.get().strip()

        if not new_username and not new_pass:
            show_error("No Changes", "Please fill in at least one field to update.")
            return
        if new_pass and len(new_pass) < 6:
            show_error("Weak Password", "Password must be at least 6 characters.")
            return
        if new_pass and new_pass != confirm_pass:
            show_error("Mismatch", "Passwords do not match.")
            return

        self.popup = ctk.CTkToplevel(self)
        self.popup.title("Confirm Update")
        self.popup.geometry("350x200")
        self.popup.grab_set()
        self.popup.configure(fg_color=COLORS["secondary"])

        ctk.CTkLabel(
            self.popup,
            text="Enter Current Password to Confirm",
            font=FONTS["label_font"],
            text_color=COLORS["text"]
        ).pack(pady=(25, 10))

        self.popup_pass_entry = ctk.CTkEntry(self.popup, width=250, show="•", placeholder_text="Current Password")
        self.popup_pass_entry.pack(pady=(0, 20))

        ctk.CTkButton(
            self.popup,
            text="Confirm",
            fg_color=COLORS["accent"],
            hover_color=COLORS["button_hover"],
            command=lambda: self.update_account(new_username, new_pass),
            width=120
        ).pack()

    # === Apply updates ===
    def update_account(self, new_username, new_pass):
        current_email = getattr(self.controller, "current_user_email", "")
        current_pass = self.popup_pass_entry.get().strip()

        if not current_email or not current_pass:
            show_error("Missing", "Current password required.")
            return

        try:
            auth = self.supabase.auth
            session = auth.sign_in_with_password({
                "email": current_email,
                "password": current_pass,
            })

            if not session.user:
                show_error("Authentication Failed", "Incorrect current password.")
                return

            update_data = {}
            if new_username:
                update_data["data"] = {"username": new_username}
            if new_pass:
                update_data["password"] = new_pass

            if not update_data:
                show_error("No Changes", "Nothing to update.")
                return

            auth.update_user(update_data)
            self.popup.destroy()
            show_info("Success", "Account updated successfully.")

            # Clear inputs
            self.entry_new_username.delete(0, "end")
            self.entry_new_pass.delete(0, "end")
            self.entry_confirm_pass.delete(0, "end")

        except Exception as e:
            show_error("Error", str(e))
