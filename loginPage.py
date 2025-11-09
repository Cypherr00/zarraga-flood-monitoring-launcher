# File: system_pages/loginPage.py
import customtkinter as ctk
from utils.dialogs import show_info, show_error
from utils.ui_styles import COLORS, get_fonts, styled_button
from navigation import go_to_main_menu

FONTS = get_fonts()

class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.supabase = controller.supabase  # use shared instance
        self.configure(fg_color=COLORS["background"])
        self.create_ui()

    def create_ui(self):
        ctk.CTkLabel(
            self,
            text="Zarraga Flood Monitoring System",
            font=FONTS["title"],
            text_color=COLORS["text"]
        ).pack(pady=(50, 10))

        ctk.CTkLabel(
            self,
            text="Login to Continue",
            font=FONTS["label_font"],
            text_color=COLORS["subtext"]
        ).pack(pady=(0, 25))

        self.email_entry = ctk.CTkEntry(
            self,
            width=320,
            placeholder_text="Email",
            font=FONTS["label_font"],
            fg_color=COLORS["secondary"],
            text_color=COLORS["text"]
        )
        self.email_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(
            self,
            width=320,
            placeholder_text="Password",
            show="•",
            font=FONTS["label_font"],
            fg_color=COLORS["secondary"],
            text_color=COLORS["text"]
        )
        self.password_entry.pack(pady=10)

        styled_button(
            self,
            text="Login",
            command=self.login_user,
            color=COLORS["button"],
            hover_color=COLORS["button_hover"],
            width=320
        ).pack(pady=20)

        ctk.CTkButton(
            self,
            text="Forgot Password?",
            width=320,
            fg_color="transparent",
            border_width=1,
            text_color=COLORS["accent"],
            hover_color=COLORS["button_hover"],
            command=self.forgot_password
        ).pack(pady=5)

    def login_user(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not email or not password:
            show_error("Missing Information", "Please enter both email and password.")
            return

        try:
            res = self.controller.supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })

            user = getattr(res, "user", None)
            if user:
                # store in controller so all pages share it
                self.controller.current_user = user
                self.controller.current_user_email = user.email
                show_info("Login Successful", f"Welcome {user.email}")
                go_to_main_menu(controller=self.controller)
            else:
                show_error("Login Failed", "Invalid email or password.")
        except Exception as e:
            show_error("Login Error", str(e))

    def forgot_password(self):
        show_info("Notice", "Function not ready yet.")
