# File: adminCreateAccount.py
import re
import customtkinter as ctk
from utils.dialogs import show_info, show_error, ask_confirm


class AdminCreateAccountPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(width=600, height=480, corner_radius=20, fg_color="#1a1a1a")

        # Title
        ctk.CTkLabel(
            self, text="Create Admin Account",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=20)

        # Username input
        ctk.CTkLabel(self, text="Username:").pack(pady=(10, 0))
        self.entry_username = ctk.CTkEntry(self, width=300)
        self.entry_username.pack(pady=(0, 10))

        # Email input
        ctk.CTkLabel(self, text="Email:").pack(pady=(10, 0))
        self.entry_email = ctk.CTkEntry(self, width=300)
        self.entry_email.pack(pady=(0, 10))

        # Password input
        ctk.CTkLabel(self, text="Password:").pack(pady=(10, 0))
        self.entry_password = ctk.CTkEntry(self, width=250, show="•")
        self.entry_password.pack(pady=(0, 10))

        # Confirm password input
        ctk.CTkLabel(self, text="Confirm Password:").pack(pady=(10, 0))
        self.entry_confirm = ctk.CTkEntry(self, width=250, show="•")
        self.entry_confirm.pack(pady=(0, 20))

        # Buttons
        ctk.CTkButton(self, text="Create", command=self.create_admin_account).pack(pady=5)
        ctk.CTkButton(
            self, text="Back",
            fg_color="#34495e", hover_color="#2c3e50",
            command=lambda: controller.show_page_from_name("SystemSettingsPage")
        ).pack(pady=5)

    def create_admin_account(self):
        username = self.entry_username.get().strip()
        email = self.entry_email.get().strip()
        password = self.entry_password.get().strip()
        confirm = self.entry_confirm.get().strip()

        # Validation
        if not username or not email or not password or not confirm:
            show_error("Missing Fields", "All fields are required.")
            return

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            show_error("Invalid Email", "Enter a valid email address.")
            return

        if password != confirm:
            show_error("Mismatch", "Passwords do not match.")
            return

        if len(password) < 6:
            show_error("Weak Password", "Password must be at least 6 characters long.")
            return

        # Confirm action
        if not ask_confirm("Confirm", f"Create account for '{email}'?"):
            return

        try:
            # Create Auth user
            result = self.controller.supabase.auth.sign_up({
                "email": email,
                "password": password,
                "options": {"data": {"username": username}}
            })

            if result.user:
                user_id = result.user.id
                # Insert into public.admin_accounts
                self.controller.supabase.table("admin_accounts").insert({
                    "uuid": user_id,
                    "username": username,
                    "email": email
                }).execute()

                show_info("Success", f"Admin account '{email}' created successfully.")

                # Clear inputs
                self.entry_username.delete(0, "end")
                self.entry_email.delete(0, "end")
                self.entry_password.delete(0, "end")
                self.entry_confirm.delete(0, "end")
            else:
                show_error("Failed", "Account could not be created.")

        except Exception as e:
            show_error("Error", str(e))
