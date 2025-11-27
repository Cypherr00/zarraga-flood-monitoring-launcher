# File: mainMenu.py
import customtkinter as ctk
import subprocess
import sys
import os
import threading
import time

from utils.dialogs import show_error, show_info
from navigation import go_to_page
from utils.ui_styles import COLORS, get_fonts, PADDING
from system_pages.systemSettings import SystemSettingsPage

FONTS = get_fonts()

class MainMenuPage(ctk.CTkFrame):
    def __init__(self, parent, controller, account_page_class=None):
        super().__init__(parent)
        self.controller = controller
        self.account_page_class = account_page_class
        self.digital_twin_process = None

        self.configure(
            width=600,
            height=400,
            corner_radius=20,
            fg_color=COLORS["background"]
        )

        # Get current user
        user_data = self.controller.supabase.auth.get_user()
        self.user = user_data.user if user_data and user_data.user else None
        username = self.user.email if self.user else "Guest"

        ctk.CTkLabel(
            self,
            text="Zarraga Flood Monitoring System",
            font=FONTS["title"],
            text_color=COLORS["text"]
        ).pack(pady=PADDING["title_y"])

        ctk.CTkLabel(
            self,
            text=f"User: {username}",
            font=FONTS["label_font"],
            text_color=COLORS["accent"],
            anchor="e"
        ).place(relx=0.98, rely=0.05, anchor="ne")

        ctk.CTkLabel(
            self,
            text="Current Water Level: -- meters",
            font=FONTS["water_level"],
            text_color=COLORS["accent"]
        ).pack(pady=PADDING["subtitle_y"])

        ctk.CTkFrame(self, height=2, width=500, fg_color=COLORS["divider"]).pack(pady=PADDING["divider_y"])

        button_width, button_spacing = 250, 15

        ctk.CTkButton(
            self, text="Open Digital Twin",
            width=button_width,
            fg_color=COLORS["button"],
            hover_color=COLORS["button_hover"],
            command=self.open_digital_twin
        ).pack(pady=button_spacing)

        ctk.CTkButton(
            self, text="Manage Accounts",
            width=button_width,
            fg_color=COLORS["button"],
            hover_color=COLORS["button_hover"],
            command=lambda: go_to_page(self.controller, self.account_page_class)
        ).pack(pady=button_spacing)

        ctk.CTkButton(
            self, text="System Settings",
            width=button_width,
            fg_color=COLORS["button"],
            hover_color=COLORS["button_hover"],
            command=self.open_settings
        ).pack(pady=button_spacing)

        ctk.CTkButton(
            self, text="Exit",
            width=button_width,
            fg_color=COLORS["danger"],
            hover_color=COLORS["danger_hover"],
            command=self.on_close
        ).pack(pady=button_spacing)

    def open_digital_twin(self):
        # Resolve correct base path (works in raw Python and PyInstaller build)
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        exe_path = os.path.join(base_path, "ZarragaFloodMonitoringAndSimulation", "Zarraga Flood Simulation.exe")

        if self.digital_twin_process and self.digital_twin_process.poll() is None:
            show_error("Notice", "Digital Twin is already running.")
            return

        if not os.path.exists(exe_path):
            show_error("Error", f"Digital Twin executable not found:\n{exe_path}")
            return

        # Create auth token file
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

        # Launch Unity exe
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
            # Cleanup token if launching fails
            for f in [auth_file, ready_file]:
                if os.path.exists(f):
                    os.remove(f)
            show_error("Error", f"Failed to open Digital Twin:\n{e}")
            return

        # Wait for Unity to signal readiness
        def wait_for_ready():
            try:
                timeout = 10  # seconds
                interval = 0.1
                elapsed = 0
                while elapsed < timeout:
                    if os.path.exists(ready_file):
                        break
                    time.sleep(interval)
                    elapsed += interval
            finally:
                # Cleanup token and ready file
                for f in [auth_file, ready_file]:
                    if os.path.exists(f):
                        try:
                            os.remove(f)
                        except:
                            pass

        threading.Thread(target=wait_for_ready, daemon=True).start()

    def open_settings(self):
        go_to_page(self.controller, SystemSettingsPage)

    def on_close(self):
        if self.digital_twin_process and self.digital_twin_process.poll() is None:
            try:
                self.digital_twin_process.terminate()
            except:
                pass
        self.controller.quit()
