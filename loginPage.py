# File: system_pages/loginPage.py
import customtkinter as ctk
import socket
import os
import sys
import time
import threading
import subprocess
import glob
from utils.dialogs import show_info, show_error
from utils.ui_styles import COLORS, get_fonts, styled_button
from navigation import go_to_main_menu

FONTS = get_fonts()

# ========================================================
# VERSION CONFIGURATION
# ========================================================
APP_VERSION = "1.1.0" 

def is_online():
    """Helper to check for internet connectivity."""
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

        # Page Configuration
        self.configure(
            fg_color=COLORS["background"],
            width=300,
            height=550,
            corner_radius=16
        )
        self.pack_propagate(False)
        
        self.create_ui()

        # Keyboard Navigation Bindings
        self.bind("<Map>", self._on_map)
        self.bind("<Unmap>", self._on_unmap)

    def _on_map(self, event):
        self.winfo_toplevel().bind("<Return>", self._handle_return)

    def _on_unmap(self, event):
        self.winfo_toplevel().unbind("<Return>")

    def _handle_return(self, event):
        if self.focus_get() == self.email_entry:
            self.password_entry.focus()
        else:
            self.login_user()

    def create_ui(self):
        # Header Section
        ctk.CTkLabel(self, text="Flood Monitoring", font=FONTS["title"], text_color=COLORS["text"]).pack(pady=(30, 4))
        ctk.CTkLabel(self, text="Sign in to continue", font=FONTS["label_font"], text_color=COLORS["subtext"]).pack(pady=(0, 20))

        # Email Input
        ctk.CTkLabel(self, text="Email", font=FONTS["label_font"], text_color=COLORS["text"]).pack(anchor="w", padx=20) 
        self.email_entry = ctk.CTkEntry(
            self, width=260, placeholder_text="Enter your email", 
            font=FONTS["label_font"], fg_color=COLORS["secondary"], text_color=COLORS["text"]
        )
        self.email_entry.pack(pady=(2, 12))

        # Password Input
        ctk.CTkLabel(self, text="Password", font=FONTS["label_font"], text_color=COLORS["text"]).pack(anchor="w", padx=20)
        self.password_entry = ctk.CTkEntry(
            self, width=260, placeholder_text="Enter your password", show="•", 
            font=FONTS["label_font"], fg_color=COLORS["secondary"], text_color=COLORS["text"]
        )
        self.password_entry.pack(pady=(2, 6))

        # Toggle Password Visibility
        self.show_pass_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            self, text="Show password", font=FONTS["label_font"], 
            text_color=COLORS["subtext"], variable=self.show_pass_var, 
            command=self.toggle_password, checkbox_width=16, checkbox_height=16, 
            border_width=2, fg_color=COLORS["accent"], hover_color=COLORS["button_hover"]
        ).pack(anchor="w", padx=20, pady=(0, 15))

        # Actions
        styled_button(
            self, text="Login", command=self.login_user, 
            color=COLORS["button"], hover_color=COLORS["button_hover"], width=260
        ).pack(pady=(10, 12))
        
        ctk.CTkButton(
            self, text="Forgot password?", width=100, fg_color="transparent", 
            border_width=0, text_color=COLORS["accent"], 
            hover_color=COLORS["button_hover"], command=self.forgot_password
        ).pack()

    def toggle_password(self):
        self.password_entry.configure(show="" if self.show_pass_var.get() else "•")

    def clear_credentials(self):
        self.email_entry.delete(0, "end")
        self.password_entry.delete(0, "end")
        self.show_pass_var.set(False)
        self.password_entry.configure(show="•")

    # ========================================================
    # SMART SYSTEM INITIALIZATION (Version-Aware Handshake)
    # ========================================================
    def pre_warm_digital_twin(self):
        """
        Launches Unity in hidden mode on first install to cache shaders/assets.
        The sentinel is stored in the install directory so it dies with an uninstall.
        """
        def run_initialization_handshake():
            # 1. FIND THE INSTALLATION ROOT
            # If frozen (compiled to exe), use the exe folder; otherwise use the script folder.
            if getattr(sys, 'frozen', False):
                app_root = os.path.dirname(sys.executable)
            else:
                # We go up one level from system_pages to reach the app root
                app_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

            # Move sentinel here so the uninstaller cleans it up automatically
            sentinel_file = os.path.join(app_root, f"init_v{APP_VERSION}.done")

            if os.path.exists(sentinel_file):
                print(f"[DEBUG] Version {APP_VERSION} already initialized. Skipping.")
                return 

            # Cleanup old 'init_v*.done' files from the root
            for old in glob.glob(os.path.join(app_root, "init_v*.done")):
                try: os.remove(old)
                except: pass

            # --- HANDSHAKE DIRECTORY ---
            appdata = os.getenv("APPDATA") or os.path.expanduser("~")
            auth_dir = os.path.join(appdata, "ZarragaFloodMonitoring")
            os.makedirs(auth_dir, exist_ok=True) 
            
            # 2. DISGUISE UI
            warmup_ui = ctk.CTkToplevel(self)
            warmup_ui.title("System Setup")
            warmup_ui.attributes("-topmost", True)
            
            w, h = 350, 180
            sw, sh = warmup_ui.winfo_screenwidth(), warmup_ui.winfo_screenheight()
            warmup_ui.geometry(f"{w}x{h}+{(sw//2)-(w//2)}+{(sh//2)-(h//2)}")
            warmup_ui.resizable(False, False)
            
            ctk.CTkLabel(warmup_ui, text="⚙️", font=("Arial", 30)).pack(pady=(20, 0))
            ctk.CTkLabel(warmup_ui, text=f"Optimizing Simulation (v{APP_VERSION})...", font=FONTS["label_font"]).pack(pady=10)
            p_bar = ctk.CTkProgressBar(warmup_ui, width=280, mode="indeterminate", progress_color=COLORS["accent"])
            p_bar.pack(pady=5)
            p_bar.start()

            auth_file = os.path.join(auth_dir, "session_auth.txt")
            ready_file = os.path.join(auth_dir, "ready.txt")
            
            try:
                # 3. PRE-CLEAN & WRITE HANDSHAKE
                for f in [auth_file, ready_file]:
                    if os.path.exists(f): os.remove(f)

                with open(auth_file, "w", encoding="utf-8") as f:
                    f.write("AUTHORIZED")
                    f.flush()
                    os.fsync(f.fileno()) # Force write to physical disk

                time.sleep(1.0) # OS stability buffer

                # 4. LAUNCH UNITY HIDDEN
                base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
                exe_path = os.path.join(base_path, "ZarragaFloodMonitoringAndSimulation", "Zarraga Flood Simulation.exe")
                
                # Use STARTUPINFO to hide the Unity window during warmup
                startup_info = subprocess.STARTUPINFO()
                startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startup_info.wShowWindow = 0 # SW_HIDE

                proc = subprocess.Popen(
                    [exe_path, "--auth-token", "AUTHORIZED"], 
                    cwd=os.path.dirname(exe_path),
                    startupinfo=startup_info
                )

                # 5. WAIT FOR READY SIGNAL
                start_time = time.time()
                timeout = 30 
                handshake_successful = False
                
                while time.time() - start_time < timeout:
                    if os.path.exists(ready_file):
                        handshake_successful = True
                        time.sleep(3.0) # Let Unity finish building caches
                        break
                    if proc.poll() is not None:
                        break
                    time.sleep(0.5)

                # 6. FORCE TERMINATION
                if proc.poll() is None:
                    proc.kill()

                # 7. MARK THIS VERSION AS DONE (In the install root)
                if handshake_successful:
                    try:
                        with open(sentinel_file, "w", encoding="utf-8") as f:
                            f.write(f"Initialized v{APP_VERSION} on {time.ctime()}")
                            f.flush()
                            os.fsync(f.fileno())
                    except PermissionError:
                        # Fallback to localappdata if install root is read-only (Program Files)
                        fallback_dir = os.path.join(os.getenv("LOCALAPPDATA"), "ZarragaFloodMonitoring")
                        os.makedirs(fallback_dir, exist_ok=True)
                        with open(os.path.join(fallback_dir, os.path.basename(sentinel_file)), "w") as f:
                            f.write("FALLBACK_PERMISSION_OK")

            except Exception as e:
                print(f"[DEBUG] Warmup Error: {e}")
            
            finally:
                time.sleep(1.0)
                for f_path in [auth_file, ready_file]:
                    if os.path.exists(f_path):
                        try: os.remove(f_path)
                        except: pass
                self.controller.after(0, warmup_ui.destroy)

        threading.Thread(target=run_initialization_handshake, daemon=True).start()

    def login_user(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not email or not password:
            show_error("Missing Information", "Please enter both email and password.")
            return

        try:
            res = self.supabase.auth.sign_in_with_password({"email": email, "password": password})
            user = getattr(res, "user", None)
            
            if user:
                self.controller.current_user = user
                self.controller.current_user_email = user.email
                self.pre_warm_digital_twin() # Trigger Handshake Check
                show_info("Login Successful", "Welcome back!")
                self.clear_credentials()
                go_to_main_menu(controller=self.controller)
            else:
                show_error("Login Failed", "Invalid credentials.")

        except Exception as e:
            # Offline Bypass for Admin
            if email == "zarraga@offline.com" and password == "admin0":
                if not is_online():
                    self.controller.current_user_email = email 
                    self.pre_warm_digital_twin()
                    show_info("Offline Mode", "Access granted.")
                    self.clear_credentials()
                    go_to_main_menu(controller=self.controller)
                else:
                    show_error("Error", "Offline account requires internet to be disabled.")
            else:
                show_error("Login Error", str(e))

    def forgot_password(self):
        email = self.email_entry.get().strip()
        if not email:
            show_error("Missing Email", "Please enter your email address.")
            return
        try:
            redirect = "https://zarraga-reset-password-vercel.vercel.app/"
            self.supabase.auth.reset_password_for_email(email, options={"redirect_to": redirect})
            show_info("Reset Email Sent", "Check your inbox.")
        except Exception as e:
            show_error("Error", str(e))