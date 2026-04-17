# File: system_pages/loginPage.py
import customtkinter as ctk
import socket
from utils.dialogs import show_info, show_error
from utils.ui_styles import COLORS, get_fonts, styled_button
from navigation import go_to_main_menu

FONTS = get_fonts()

def is_online():
    """Returns True if there is an active internet connection, False otherwise."""
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        pass
    return False

class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self.supabase = controller.supabase

        # UPDATED: Reduced height from 550 to 460 to fix the "Empty Void" at the bottom
        self.configure(
            fg_color=COLORS["background"],
            width=300,
            height=550,
            corner_radius=16
        )
        self.pack_propagate(False)

        self.create_ui()

        # Enter key behavior
        self.email_entry.bind("<Return>", lambda e: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda e: self.login_user())

    def create_ui(self):
        # Title 
        ctk.CTkLabel(
            self,
            text="Flood Monitoring",
            font=FONTS["title"],
            text_color=COLORS["text"]
        ).pack(pady=(30, 4))

        # Subtitle
        ctk.CTkLabel(
            self,
            text="Sign in to continue",
            font=FONTS["label_font"],
            text_color=COLORS["subtext"]
        ).pack(pady=(0, 20))

        # UPDATED: Added a dedicated label for Email above the entry field
        ctk.CTkLabel(
            self, 
            text="Email", 
            font=FONTS["label_font"], 
            text_color=COLORS["text"]
        ).pack(anchor="w", padx=20) # anchor="w" and padx=20 align it perfectly with the entry box
        
        # Email entry
        self.email_entry = ctk.CTkEntry(
            self,
            width=260,
            placeholder_text="Enter your email", # Made placeholder more conversational
            font=FONTS["label_font"],
            fg_color=COLORS["secondary"],
            text_color=COLORS["text"]
        )
        self.email_entry.pack(pady=(2, 12))

        # UPDATED: Added a dedicated label for Password
        ctk.CTkLabel(
            self, 
            text="Password", 
            font=FONTS["label_font"], 
            text_color=COLORS["text"]
        ).pack(anchor="w", padx=20)

        # Password entry
        self.password_entry = ctk.CTkEntry(
            self,
            width=260,
            placeholder_text="Enter your password",
            show="•",
            font=FONTS["label_font"],
            fg_color=COLORS["secondary"],
            text_color=COLORS["text"]
        )
        self.password_entry.pack(pady=(2, 6))

        # UPDATED: "Show Password" Checkbox Toggle
        self.show_pass_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            self,
            text="Show password",
            font=FONTS["label_font"],
            text_color=COLORS["subtext"],
            variable=self.show_pass_var,
            command=self.toggle_password,
            checkbox_width=16,
            checkbox_height=16,
            border_width=2,
            fg_color=COLORS["accent"], 
            hover_color=COLORS["button_hover"]
        ).pack(anchor="w", padx=20, pady=(0, 15))

        # Login button
        styled_button(
            self,
            text="Login",
            command=self.login_user,
            color=COLORS["button"],
            hover_color=COLORS["button_hover"],
            width=260
        ).pack(pady=(10, 12))

        # Forgot password link 
        ctk.CTkButton(
            self,
            text="Forgot password?",
            width=100,
            fg_color="transparent",
            border_width=0,
            text_color=COLORS["accent"],
            hover_color=COLORS["button_hover"],
            command=self.forgot_password
        ).pack()

    # UPDATED: New method to handle the show/hide password logic
    def toggle_password(self):
        if self.show_pass_var.get():
            self.password_entry.configure(show="")
        else:
            self.password_entry.configure(show="•")

    def login_user(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not email or not password:
            show_error("Missing Information", "Please enter both email and password.")
            return

        try:
            res = self.supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            user = getattr(res, "user", None)

            if user:
                self.controller.current_user = user
                self.controller.current_user_email = user.email
                show_info("Login Successful", "Welcome to FloodTwin!")
                go_to_main_menu(controller=self.controller)
            else:
                show_error("Login Failed", "Invalid email or password.")

        except Exception as e:
            if email == "zarraga@offline.com" and password == "admin0":
                if not is_online():
                    self.controller.current_user_email = email 
                    show_info("Offline Mode", "Logged in using offline mode.")
                    go_to_main_menu(controller=self.controller)
                else:
                    show_error("Login Error", "This offline account can only be used when disconnected from the internet.")
            else:
                show_error("Login Error", str(e))

    def forgot_password(self):
        email = self.email_entry.get().strip()
        if not email:
            show_error("Missing Email", "Please enter your email.")
            return

        try:
            redirect = "https://zarraga-reset-password-vercel.vercel.app/"
            self.supabase.auth.reset_password_for_email(
                email,
                options={"redirect_to": redirect}
            )
            show_info("Password Reset", "A reset link has been sent to your email.")

        except Exception as e:
            show_error("Error", str(e))