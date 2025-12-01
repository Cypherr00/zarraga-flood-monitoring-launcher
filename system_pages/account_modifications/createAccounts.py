import re
import customtkinter as ctk
from utils.dialogs import show_info, show_error, ask_confirm
from utils.ui_styles import COLORS

class CreateAccountsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(width=600, height=400, corner_radius=20, fg_color=COLORS["background"])

        # Title
        ctk.CTkLabel(
            self, text="Create Account",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=20)

        # Username input
        ctk.CTkLabel(self, text="Username:").pack(pady=(10, 0))
        self.entry_username = ctk.CTkEntry(self, width=250)
        self.entry_username.pack(pady=(0, 10))

        # PIN input (visible, restricted to 4 digits)
        ctk.CTkLabel(self, text="PIN (4 digits):").pack(pady=(10, 0))
        self.entry_pin = ctk.CTkEntry(self, width=120, justify="center")
        self.entry_pin.pack(pady=(0, 20))

        # Apply validation
        self._apply_pin_validation()

        # Buttons
        ctk.CTkButton(self, text="Create", command=self.create_account).pack(pady=5)
        ctk.CTkButton(
            self, text="Back",
            fg_color="#34495e", hover_color="#2c3e50",
            command=lambda: controller.show_page("AccountManagerPage")
        ).pack(pady=5)

    def _apply_pin_validation(self):
        """Restrict PIN entry to digits only, maximum 4."""
        def validate_input(P):
            return bool(re.match(r'^\d{0,4}$', P))
        vcmd = (self.register(validate_input), "%P")
        self.entry_pin.configure(validate="key", validatecommand=vcmd)

    def create_account(self):
        username = self.entry_username.get().strip()
        pin = self.entry_pin.get().strip()

        # Validation
        if not username or not pin:
            show_error("Missing Fields", "All fields are required.")
            return

        if not pin.isdigit() or len(pin) != 4:
            show_error("Invalid PIN", "PIN must be exactly 4 digits long.")
            return

        # Confirmation before saving
        if not ask_confirm("Confirm", f"Create account for '{username}' with this PIN?"):
            return

        try:
            response = self.controller.supabase.table("user").insert({
                "user_name": username,
                "pin": pin
            }).execute()

            if response.data:
                show_info("Success", f"Account '{username}' created successfully.")
                self.entry_username.delete(0, "end")
                self.entry_pin.delete(0, "end")
            else:
                show_error("Failed", "Account could not be created.")
        except Exception as e:
            show_error("Database Error", str(e))
