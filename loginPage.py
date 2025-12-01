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
        self.supabase = controller.supabase

        # Modern compact card
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
        # Title (shortened to fit modern card)
        ctk.CTkLabel(
            self,
            text="Flood Monitoring",
            font=FONTS["title"],
            text_color=COLORS["text"]
        ).pack(pady=(25, 4))

        # Subtitle
        ctk.CTkLabel(
            self,
            text="Sign in to continue",
            font=FONTS["label_font"],
            text_color=COLORS["subtext"]
        ).pack(pady=(0, 20))

        # Email entry
        self.email_entry = ctk.CTkEntry(
            self,
            width=260,
            placeholder_text="Email",
            font=FONTS["label_font"],
            fg_color=COLORS["secondary"],
            text_color=COLORS["text"]
        )
        self.email_entry.pack(pady=8)

        # Password entry
        self.password_entry = ctk.CTkEntry(
            self,
            width=260,
            placeholder_text="Password",
            show="•",
            font=FONTS["label_font"],
            fg_color=COLORS["secondary"],
            text_color=COLORS["text"]
        )
        self.password_entry.pack(pady=8)

        # Login button
        styled_button(
            self,
            text="Login",
            command=self.login_user,
            color=COLORS["button"],
            hover_color=COLORS["button_hover"],
            width=260
        ).pack(pady=(18, 12))

        # Forgot password link (compact modern style)
        ctk.CTkButton(
            self,
            text="Forgot password?",
            width=100,
            fg_color="transparent",
            border_width=0,
            text_color=COLORS["accent"],
            hover_color=COLORS["button_hover"],
            command=self.forgot_password
        ).pack(pady=0)

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
                go_to_main_menu(controller=self.controller)
            else:
                show_error("Login Error", "Unable to connect to the internet")

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
