# File: system_pages/loginPage.py
import customtkinter as ctk
import socket
import os
import time
import threading
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

        # UI Configuration
        self.configure(
            fg_color=COLORS["background"],
            width=300,
            height=550,
            corner_radius=16
        )
        self.pack_propagate(False)

        self.create_ui()

        # Bind Enter key globally when the page is active
        self.bind("<Map>", self._on_map)
        self.bind("<Unmap>", self._on_unmap)

    def _on_map(self, event):
        """When the page is shown, bind the Enter key to the main window."""
        self.winfo_toplevel().bind("<Return>", self._handle_return)

    def _on_unmap(self, event):
        """When leaving the page, remove the binding so it doesn't affect other pages."""
        self.winfo_toplevel().unbind("<Return>")

    def _handle_return(self, event):
        """If focus is on the email entry, move to password. Otherwise, try to log in."""
        if self.focus_get() == self.email_entry:
            self.password_entry.focus()
        else:
            self.login_user()

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

        # Email Label
        ctk.CTkLabel(
            self, 
            text="Email", 
            font=FONTS["label_font"], 
            text_color=COLORS["text"]
        ).pack(anchor="w", padx=20) 
        
        # Email entry
        self.email_entry = ctk.CTkEntry(
            self,
            width=260,
            placeholder_text="Enter your email", 
            font=FONTS["label_font"],
            fg_color=COLORS["secondary"],
            text_color=COLORS["text"]
        )
        self.email_entry.pack(pady=(2, 12))

        # Password Label
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

        # Show Password Checkbox
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

    def toggle_password(self):
        if self.show_pass_var.get():
            self.password_entry.configure(show="")
        else:
            self.password_entry.configure(show="•")

    def clear_credentials(self):
        """Clears the email and password fields for security upon successful login."""
        self.email_entry.delete(0, "end")
        self.password_entry.delete(0, "end")
        self.show_pass_var.set(False)
        self.password_entry.configure(show="•")

    def pre_warm_digital_twin(self):
        """
        Background task to 'pre-heat' the file system.
        This forces Windows Defender to scan the folder and the OS to cache 
        the handshake path before the user actually tries to launch the simulation.
        """
        def run_warmup():
            appdata = os.getenv("APPDATA") or os.path.expanduser("~")
            auth_dir = os.path.join(appdata, "ZarragaFloodMonitoring")
            
            try:
                # Ensure directory exists
                if not os.path.exists(auth_dir):
                    os.makedirs(auth_dir, exist_ok=True)
                    time.sleep(0.2)

                auth_file = os.path.join(auth_dir, "session_auth.txt")
                
                # Write a dummy handshake to trigger OS indexing/Antivirus scan
                with open(auth_file, "w", encoding="utf-8") as f:
                    f.write("WARMING_UP")
                    f.flush()
                    os.fsync(f.fileno())
                
                # Brief pause, then read it back to verify access
                time.sleep(0.3)
                if os.path.exists(auth_file):
                    with open(auth_file, "r") as f:
                        _ = f.read()
                
                # Cleanup: Leave the environment 'warm' but clean
                os.remove(auth_file)
            except Exception:
                pass 

        # Execute in background to keep UI responsive
        threading.Thread(target=run_warmup, daemon=True).start()

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
                
                # Warm up the file system for the Digital Twin
                self.pre_warm_digital_twin()
                
                show_info("Login Successful", "Welcome to FloodTwin!")
                self.clear_credentials()
                go_to_main_menu(controller=self.controller)
            else:
                show_error("Login Failed", "Invalid email or password.")

        except Exception as e:
            # Handle Offline Mode Check
            if email == "zarraga@offline.com" and password == "admin0":
                if not is_online():
                    self.controller.current_user_email = email 
                    self.pre_warm_digital_twin()
                    show_info("Offline Mode", "Logged in using offline mode.")
                    self.clear_credentials()
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