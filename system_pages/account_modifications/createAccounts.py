import re
import customtkinter as ctk
from utils.dialogs import show_info, show_error, ask_confirm
from utils.ui_styles import COLORS

class CreateAccountsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # RESTORED: Explicit sizing for the narrow 300x550 mobile-style frame
        self.configure(width=300, height=550, fg_color=COLORS["background"], corner_radius=20)
        self.pack_propagate(False)

        # =========================================
        # TOP HEADER
        # =========================================
        top_bar = ctk.CTkFrame(self, fg_color="transparent")
        top_bar.pack(fill="x", padx=15, pady=(15, 5))

        # Back button 
        ctk.CTkButton(
            top_bar, text="◄ Back", width=60,
            fg_color="transparent", hover_color=COLORS["secondary"],
            text_color=COLORS["text"], font=ctk.CTkFont(size=14, weight="bold"),
            command=lambda: self.controller.show_page("AccountManagerPage")
        ).pack(side="left")

        # =========================================
        # FORM CONTAINER (Centered Vertically)
        # =========================================
        form_container = ctk.CTkFrame(self, fg_color="transparent")
        form_container.place(relx=0.5, rely=0.45, anchor="center") # Slightly raised to balance the back button

        # Title
        ctk.CTkLabel(
            form_container, text="Create Account",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=COLORS["text"]
        ).pack(pady=(0, 25))

        # Username Input
        ctk.CTkLabel(
            form_container, text="Username:", 
            font=ctk.CTkFont(size=14), text_color=COLORS["text"], anchor="w"
        ).pack(fill="x", padx=10, pady=(0, 5))
        
        self.entry_username = ctk.CTkEntry(
            form_container, width=240, height=40,
            fg_color=COLORS["secondary"], text_color=COLORS["text"]
        )
        self.entry_username.pack(padx=10, pady=(0, 15))

        # PIN Input
        ctk.CTkLabel(
            form_container, text="PIN (4 digits):", 
            font=ctk.CTkFont(size=14), text_color=COLORS["text"], anchor="w"
        ).pack(fill="x", padx=10, pady=(0, 5))
        
        self.entry_pin = ctk.CTkEntry(
            form_container, width=240, height=40, justify="center",
            fg_color=COLORS["secondary"], text_color=COLORS["text"]
        )
        self.entry_pin.pack(padx=10, pady=(0, 30))

        # Apply regex validation
        self._apply_pin_validation()

        # Submit Button
        ctk.CTkButton(
            form_container, text="Create Account", width=240, height=45,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=COLORS["button"], hover_color=COLORS["button_hover"],
            command=self.create_account
        ).pack(padx=10, pady=(0, 10))


    # =========================================
    # LOGIC
    # =========================================
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

        if len(pin) != 4:
            show_error("Invalid PIN", "PIN must be exactly 4 digits long.")
            return

        # Confirmation before saving
        if not ask_confirm("Confirm", f"Create account for '{username}'?"):
            return

        try:
            # Explicitly setting is_active to True for the new database structure
            response = self.controller.supabase.table("user").insert({
                "user_name": username,
                "pin": pin,
                "is_active": True  
            }).execute()

            if response.data:
                show_info("Success", f"Account '{username}' created successfully.")
                self.entry_username.delete(0, "end")
                self.entry_pin.delete(0, "end")
                self.entry_username.focus()
            else:
                show_error("Failed", "Account could not be created.")
                
        except Exception as e:
            show_error("Database Error", f"Failed to create account.\n\nReason: {str(e)}")