# File: mainMenu.py
import customtkinter as ctk
import subprocess
import sys
import os
import threading
import time
from PIL import Image, ImageTk  # for logo

from utils.dialogs import show_error, show_info
from navigation import go_to_page
from utils.ui_styles import COLORS, get_fonts, PADDING
from loginPage import LoginPage      # needed for logout redirect
from system_pages.systemSettings import SystemSettingsPage

FONTS = get_fonts()

class MainMenuPage(ctk.CTkFrame):
    def __init__(self, parent, controller, account_page_class=None):
        super().__init__(parent)
        self.controller = controller
        self.account_page_class = account_page_class
        self.digital_twin_process = None

        self.configure(
            width=300,
            height=550,
            corner_radius=0,
            fg_color=COLORS["background"]
        )
        self.pack_propagate(False)

        # =============================
        # TOP LOGO
        # =============================
        try:
            logo_image = Image.open("assets/icon-logo.png")
            logo_image = logo_image.resize((120, 120))
            self.logo_photo = ImageTk.PhotoImage(logo_image)
            ctk.CTkLabel(self, image=self.logo_photo, text="").pack(pady=(40, 20))
        except Exception as e:
            # fallback: show text if logo fails
            ctk.CTkLabel(
                self,
                text="Zarraga Flood Monitoring System",
                font=FONTS["title"],
                text_color=COLORS["text"]
            ).pack(pady=(40, 20))

        # =============================
        # DIGITAL TWIN LABEL + BUTTON
        # =============================
        
        ctk.CTkButton(
            self,
            text="▶",
            width=100,
            height=50,
            corner_radius=15,  # less round
            fg_color=COLORS["button"],
            hover_color=COLORS["button_hover"],
            font=("Arial", 40),
            command=self.open_digital_twin
        ).pack(pady=(50, 0))
        
        ctk.CTkLabel(
                    self,
                    text="Digital Twin",
                    font=("Arial", 25, "bold"),
                    text_color="#043E71"
                ).pack(pady=(0, 10))
        # =============================
        # BOTTOM-LEFT ICON BUTTONS
        # =============================
        bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_frame.place(x=15, y=450)  # adjust y if needed

        button_frame = ctk.CTkFrame(
            bottom_frame,
            fg_color=COLORS["secondary"],
            corner_radius=10
        )
        button_frame.pack()

        btn_size = 40

        # Account button (upper)
        ctk.CTkButton(
            button_frame,
            text="👤",
            width=btn_size,
            height=btn_size,
            fg_color=COLORS["button"],
            hover_color=COLORS["button_hover"],
            corner_radius=8,
            font=("Arial", 22),
            command=lambda: go_to_page(self.controller, self.account_page_class)
        ).pack(pady=(8, 4), padx=10)

        # Logout button (bottom)
        ctk.CTkButton(
            button_frame,
            text="🚪",
            width=btn_size,
            height=btn_size,
            fg_color=COLORS["button"],
            hover_color=COLORS["button_hover"],
            corner_radius=8,
            font=("Arial", 22),
            command=self.logout
        ).pack(pady=(4, 8), padx=10)

    # ======================================================
    # LOGOUT
    # ======================================================
    def logout(self):
        try:
            self.controller.supabase.auth.sign_out()
        except Exception as e:
            show_error("Logout Failed", str(e))
            return
        go_to_page(self.controller, LoginPage)

    # ======================================================
    # DIGITAL TWIN LOGIC
    # ======================================================
    def open_digital_twin(self):
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        exe_path = os.path.join(base_path, "ZarragaFloodMonitoringAndSimulation", "Zarraga Flood Simulation.exe")

        if self.digital_twin_process and self.digital_twin_process.poll() is None:
            show_error("Notice", "Digital Twin is already running.")
            return

        if not os.path.exists(exe_path):
            show_error("Error", f"Digital Twin executable not found:\n{exe_path}")
            return

        appdata = os.getenv("APPDATA") or os.path.expanduser("~")
        auth_dir = os.path.join(appdata, "ZarragaFloodMonitoring")
        os.makedirs(auth_dir, exist_ok=True)
        auth_file = os.path.join(auth_dir, "session_auth.txt")
        ready_file = os.path.join(auth_dir, "ready.txt")

        try:
            with open(auth_file, "w", encoding="utf-8") as f:
                f.write("AUTHORIZED")
        except Exception as e:
            show_error("Error", f"Unable to create auth token:\n{e}")
            return

        try:
            creationflags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
            self.digital_twin_process = subprocess.Popen(
                [exe_path],
                shell=False,
                creationflags=creationflags,
                cwd=os.path.dirname(exe_path)
            )
            show_info("Launching", "Digital Twin is starting...")
        except Exception as e:
            for f in [auth_file, ready_file]:
                if os.path.exists(f):
                    os.remove(f)
            show_error("Error", f"Failed to open Digital Twin:\n{e}")
            return

        def wait_for_ready():
            try:
                timeout = 10
                interval = 0.1
                elapsed = 0
                while elapsed < timeout:
                    if os.path.exists(ready_file):
                        break
                    time.sleep(interval)
                    elapsed += interval
            finally:
                for f in [auth_file, ready_file]:
                    if os.path.exists(f):
                        try:
                            os.remove(f)
                        except:
                            pass

        threading.Thread(target=wait_for_ready, daemon=True).start()
