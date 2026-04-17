# File: mainMenu.py
import customtkinter as ctk
import subprocess
import sys
import os
import threading
import time
from PIL import Image, ImageTk

from utils.dialogs import show_error, show_info
from navigation import go_to_page
from utils.ui_styles import COLORS, get_fonts, PADDING
from loginPage import LoginPage
from system_pages.systemSettings import SystemSettingsPage

FONTS = get_fonts()


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class MainMenuPage(ctk.CTkFrame):
    def __init__(self, parent, controller, account_page_class=None):
        super().__init__(parent)
        self.controller = controller
        self.account_page_class = account_page_class
        self.digital_twin_process = None

        self.configure(
            width=300,
            height=560, # Adjusted to 560 to match your full vertical stretch
            corner_radius=0,
            fg_color=COLORS["background"]
        )
        self.pack_propagate(False)

        # Structure the layout into three distinct vertical zones
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_frame.pack(side="top", fill="x", pady=(30, 10))

        self.middle_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.middle_frame.pack(side="top", fill="both", expand=True) # expand=True centers the content

        self.bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.bottom_frame.pack(side="bottom", fill="x", pady=(0, 30))

        self.create_ui()

    def create_ui(self):
        # =========================================
        # TOP: LOGO SECTION
        # =========================================
        logo_path = resource_path("assets/icon-logo.png")
        
        try:
            logo_image = Image.open(logo_path)
            logo_image = logo_image.resize((100, 100)) # Slightly smaller for a cleaner look
            self.logo_photo = ImageTk.PhotoImage(logo_image)

            ctk.CTkLabel(self.top_frame, image=self.logo_photo, text="").pack()
        except Exception as e:
            print("[DEBUG] Logo load error:", e)
            ctk.CTkLabel(
                self.top_frame,
                text="FloodTwin",
                font=FONTS["title"],
                text_color=COLORS["text"]
            ).pack()

        # Separator Line (adds a premium touch)
        ctk.CTkFrame(
            self.top_frame, 
            height=2, 
            fg_color=COLORS["secondary"]
        ).pack(fill="x", padx=30, pady=(20, 0))


        # =========================================
        # MIDDLE: DIGITAL TWIN ACTION AREA
        # =========================================
        # Wrapping it in a card to make it look like a dashboard widget
        action_card = ctk.CTkFrame(
            self.middle_frame, 
            fg_color=COLORS["secondary"], 
            corner_radius=16
        )
        action_card.place(relx=0.5, rely=0.5, anchor="center") # Perfectly centers the card

        ctk.CTkLabel(
            action_card,
            text="Digital Twin",
            font=("Arial", 20, "bold"),
            text_color=COLORS["text"]
        ).pack(pady=(20, 10))

        # The large play button
        ctk.CTkButton(
            action_card,
            text="▶",
            width=80,
            height=60,
            corner_radius=12,
            fg_color=COLORS["button"],
            hover_color=COLORS["button_hover"],
            font=("Arial", 30),
            command=self.open_digital_twin
        ).pack(pady=(0, 20), padx=40)


        # =========================================
        # BOTTOM: NAVIGATION BUTTONS
        # =========================================
        # Using a transparent/flat button style so they don't compete with the Play button
        btn_width = 240
        btn_height = 40
        btn_font = ("Arial", 14, "bold")

        ctk.CTkButton(
            self.bottom_frame,
            text="👤    My Account",
            width=btn_width,
            height=btn_height,
            fg_color="transparent", # Transparent default
            hover_color=COLORS["secondary"], # Highlights on hover
            text_color=COLORS["text"],
            corner_radius=8,
            font=btn_font,
            anchor="w",
            command=lambda: go_to_page(self.controller, self.account_page_class)
        ).pack(pady=(0, 5))

        ctk.CTkButton(
            self.bottom_frame,
            text="⚙️    Settings", # Added a settings placeholder just to balance the menu
            width=btn_width,
            height=btn_height,
            fg_color="transparent",
            hover_color=COLORS["secondary"],
            text_color=COLORS["text"],
            corner_radius=8,
            font=btn_font,
            anchor="w",
            command=lambda: go_to_page(self.controller, SystemSettingsPage)
        ).pack(pady=(0, 5))

        ctk.CTkButton(
            self.bottom_frame,
            text="🚪    Logout",
            width=btn_width,
            height=btn_height,
            fg_color="transparent",
            hover_color="#5c1a1a", # Subtle red hue on hover for destructive action
            text_color=COLORS["accent"], # Use accent color (or a distinct color)
            corner_radius=8,
            font=btn_font,
            anchor="w",
            command=self.logout
        ).pack()


    # =========================================
    # LOGOUT LOGIC
    # =========================================
    def logout(self):
        import tkinter as tk
        from tkinter import messagebox

        confirm_root = tk.Tk()
        confirm_root.withdraw()

        confirm = messagebox.askyesno(
            "Confirm Logout",
            "Are you sure you want to log out?"
        )

        confirm_root.destroy()

        if not confirm:
            return

        try:
            self.controller.supabase.auth.sign_out()
        except Exception as e:
            show_error("Logout Failed", str(e))
            return

        go_to_page(self.controller, LoginPage)


    # =========================================
    # DIGITAL TWIN LOGIC
    # =========================================
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