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

        # Base container
        self.configure(
            width=400,
            height=500,
            corner_radius=0,
            
        )

        # Top bar container (clean modern bar)
        top_bar = ctk.CTkFrame(
            self,
            height=50,
            fg_color=COLORS["background"],
            corner_radius=0
        )
        top_bar.pack(fill="x", side="top")

        # App Title on left side of top bar
        ctk.CTkLabel(
            top_bar,
            text="Zarraga Flood Monitoring System",
            font=FONTS["title"],
            text_color=COLORS["text"],
            anchor="w"
        ).pack(side="left", padx=20, pady=10)

        # Top-right settings icon button
        # (Replaces 'User: username' text completely)
        settings_icon = ctk.CTkButton(
            top_bar,
            width=40,
            height=40,
            text="⚙",                      # Minimal gear icon
            font=FONTS["label_font"],
            fg_color=COLORS["button"],
            hover_color=COLORS["button_hover"],
            corner_radius=8,
            command=self.open_settings
        )
        settings_icon.pack(side="right", padx=15, pady=5)

        # Main content container (left-aligned buttons + info)
        content_frame = ctk.CTkFrame(
            self,
            fg_color=COLORS["background"]
        )
        content_frame.pack(fill="both", expand=True, padx=30, pady=20)

        # Left column where all buttons will be aligned
        left_menu = ctk.CTkFrame(
            content_frame,
            width=250,
            fg_color=COLORS["background"]
        )
        left_menu.pack(side="left", anchor="n", pady=10)

        # Water level info panel (aligned left above menu buttons)
        water_panel = ctk.CTkFrame(
            left_menu,
            fg_color=COLORS["secondary"],
            corner_radius=12
        )
        water_panel.pack(fill="x", pady=(0, 20))

        self.water_label = ctk.CTkLabel(
            water_panel,
            text="Current Water Level: -- meters",
            font=FONTS["water_level"],
            text_color=COLORS["text"],
            anchor="w"
        )
        self.water_label.pack(padx=15, pady=10)

        # Modern left-aligned buttons
        button_width = 220
        button_pad = 10

        ctk.CTkButton(
            left_menu,
            text="Open Digital Twin",
            width=button_width,
            text_color=COLORS["text"],
            fg_color=COLORS["button"],
            hover_color=COLORS["button_hover"],
            anchor="w",
            command=self.open_digital_twin
        ).pack(fill="x", pady=button_pad)

        ctk.CTkButton(
            left_menu,
            text="Manage Accounts",
            width=button_width,
            text_color=COLORS["text"],
            fg_color=COLORS["button"],
            hover_color=COLORS["button_hover"],
            anchor="w",
            command=lambda: go_to_page(self.controller, self.account_page_class)
        ).pack(fill="x", pady=button_pad)

        # Exit button is separated to indicate destructive action
        ctk.CTkButton(
            left_menu,
            text="Exit",
            width=button_width,
            fg_color=COLORS["danger"],
            hover_color=COLORS["danger_hover"],
            anchor="w",
            command=self.on_close
        ).pack(fill="x", pady=(30, 0))

    # ==========================================================
    #                    DIGITAL TWIN FUNCTION
    # ==========================================================
    def open_digital_twin(self):
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        exe_path = os.path.join(base_path, "ZarragaFloodMonitoringAndSimulation", "Zarraga Flood Simulation.exe")

        if self.digital_twin_process and self.digital_twin_process.poll() is None:
            show_error("Notice", "Digital Twin is already running.")
            return

        if not os.path.exists(exe_path):
            show_error("Error", f"Digital Twin executable not found:\n{exe_path}")
            return

        # Authentication files
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

        # Wait for Unity 'ready' signal
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

    # ==========================================================
    #                      OPEN SETTINGS
    # ==========================================================
    def open_settings(self):
        go_to_page(self.controller, SystemSettingsPage)

    # ==========================================================
    #                          EXIT
    # ==========================================================
    def on_close(self):
        if self.digital_twin_process and self.digital_twin_process.poll() is None:
            try:
                self.digital_twin_process.terminate()
            except:
                pass
        self.controller.quit()
