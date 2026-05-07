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
            height=560,
            corner_radius=0,
            fg_color=COLORS["background"]
        )
        self.pack_propagate(False)

        # Structure the layout into three distinct vertical zones
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_frame.pack(side="top", fill="x", pady=(30, 10))

        self.middle_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.middle_frame.pack(side="top", fill="both", expand=True)

        self.bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.bottom_frame.pack(side="bottom", fill="x", pady=(0, 30))

        self.create_ui()

    def create_ui(self):
        # =========================================
        # TOP: LOGO & HOME LABEL
        # =========================================
        logo_path = resource_path("assets/icon-logo.png")
        
        try:
            logo_image = Image.open(logo_path)
            logo_image = logo_image.resize((100, 100))
            self.logo_photo = ImageTk.PhotoImage(logo_image)

            ctk.CTkLabel(self.top_frame, image=self.logo_photo, text="").pack(pady=(0, 5))
        except Exception as e:
            print("[DEBUG] Logo load error:", e)
            ctk.CTkLabel(
                self.top_frame,
                text="FloodTwin",
                font=FONTS["title"],
                text_color=COLORS["text"]
            ).pack(pady=(0, 5))

        # Home Label indicator (using subtext color for a softer look)
        ctk.CTkLabel(
            self.top_frame,
            text="H O M E",
            font=("Arial", 11, "bold"),
            text_color=COLORS["subtext"]
        ).pack(pady=(0, 5))

        # Separator Line (Now using your specific divider color)
        ctk.CTkFrame(
            self.top_frame, 
            height=2, 
            fg_color=COLORS["divider"]
        ).pack(fill="x", padx=40, pady=(15, 0))


        # =========================================
        # MIDDLE: DIGITAL TWIN ACTION CARD
        # =========================================
        # Adjusted rely to 0.45 for perfect vertical balance
        self.action_card = ctk.CTkFrame(
            self.middle_frame, 
            fg_color=COLORS["button"], 
            corner_radius=12, # Slightly sharper corners for a modern tech look
            cursor="hand2"
        )
        self.action_card.place(relx=0.5, rely=0.45, anchor="center")

        def trigger_action(event):
            self.open_digital_twin()

        # Left side: Play Icon (White for high contrast against blue)
        icon_label = ctk.CTkLabel(
            self.action_card,
            text="▶",
            font=("Arial", 36),
            text_color="white" 
        )
        icon_label.grid(row=0, column=0, rowspan=2, padx=(25, 15), pady=20)

        # Right side: Title text (White for readability)
        title_label = ctk.CTkLabel(
            self.action_card,
            text="Digital Twin",
            font=("Arial", 18, "bold"),
            text_color="white"
        )
        title_label.grid(row=0, column=1, sticky="sw", padx=(0, 30), pady=(20, 0))

        # Right side: Subtitle text (Using divider color as a soft light-blue accent)
        subtitle_label = ctk.CTkLabel(
            self.action_card,
            text="Launch Unity",
            font=("Arial", 12),
            text_color=COLORS["divider"] 
        )
        subtitle_label.grid(row=1, column=1, sticky="nw", padx=(0, 30), pady=(0, 20))

        # Bind hover effects
        card_widgets = [self.action_card, icon_label, title_label, subtitle_label]
        for widget in card_widgets:
            widget.bind("<Button-1>", trigger_action)
            widget.bind("<Enter>", lambda e: self.action_card.configure(fg_color=COLORS["button_hover"]))
            widget.bind("<Leave>", lambda e: self.action_card.configure(fg_color=COLORS["button"]))


        # =========================================
        # BOTTOM: NAVIGATION BUTTONS
        # =========================================
        btn_width = 240
        btn_height = 42
        btn_font = ("Arial", 14, "bold")

        # Users Button
        ctk.CTkButton(
            self.bottom_frame,
            text="👤    Users",
            width=btn_width,
            height=btn_height,
            fg_color="transparent",
            hover_color=COLORS["secondary"],
            text_color=COLORS["text"],
            corner_radius=8,
            font=btn_font,
            anchor="w",
            command=lambda: go_to_page(self.controller, self.account_page_class)
        ).pack(pady=(0, 8))

        # Logout Button (Now uses your DANGER_COLOR for clear UI semantics)
        ctk.CTkButton(
            self.bottom_frame,
            text="🚪    Logout",
            width=btn_width,
            height=btn_height,
            fg_color="transparent",
            hover_color=COLORS["secondary"], # Soft hover to match light theme
            text_color=COLORS["danger"], # Red text for destructive action
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
    # =========================================def open_digital_twin(self):
        import time
        import threading
        import tkinter as tk # Still needed for some screen metrics

        base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        exe_path = os.path.join(base_path, "ZarragaFloodMonitoringAndSimulation", "Zarraga Flood Simulation.exe")

        if self.digital_twin_process and self.digital_twin_process.poll() is None:
            show_error("Notice", "Digital Twin is already running.")
            return

        if not os.path.exists(exe_path):
            show_error("Error", f"Digital Twin executable not found:\n{exe_path}")
            return

        # Prepare Shared Mailbox Paths
        appdata = os.getenv("APPDATA") or os.path.expanduser("~")
        auth_dir = os.path.join(appdata, "ZarragaFloodMonitoring")
        auth_file = os.path.join(auth_dir, "session_auth.txt")
        ready_file = os.path.join(auth_dir, "ready.txt")

        # 1. THE HANDSHAKE (Writing the Key)
        try:
            os.makedirs(auth_dir, exist_ok=True)
            with open(auth_file, "w", encoding="utf-8") as f:
                f.write("AUTHORIZED")
                f.flush()
                os.fsync(f.fileno())
        except Exception as e:
            show_error("Error", f"Handshake failed: {e}")
            return

        # 2. CREATE MODERN UI ALERT
        # We use CTkToplevel so it matches your theme (Dark/Light)
        loading_win = ctk.CTkToplevel(self)
        loading_win.title("Launching Simulation")
        loading_win.attributes("-topmost", True)
        
        # Geometry sizing and centering
        win_w, win_h = 400, 200
        screen_w = loading_win.winfo_screenwidth()
        screen_h = loading_win.winfo_screenheight()
        loading_win.geometry(f"{win_w}x{win_h}+{(screen_w//2)-(win_w//2)}+{(screen_h//2)-(win_h//2)}")
        loading_win.resizable(False, False)

        # UI Content for the Alert Box
        ctk.CTkLabel(loading_win, text="🌊", font=("Arial", 40)).pack(pady=(20, 5))
        ctk.CTkLabel(loading_win, text="Starting Digital Twin...", font=FONTS["title"]).pack(pady=5)
        
        # The Progress Bar (Indeterminate means it slides back and forth)
        progress = ctk.CTkProgressBar(loading_win, width=320, mode="indeterminate", progress_color=COLORS["accent"])
        progress.pack(pady=15)
        progress.start()

        # 3. BACKGROUND EXECUTION (This is why the code looks cleaner)
        def launch_and_monitor():
            try:
                # Start Unity
                creationflags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
                self.digital_twin_process = subprocess.Popen(
                    [exe_path],
                    cwd=os.path.dirname(exe_path),
                    creationflags=creationflags
                )

                # Wait for Unity to say "I'm ready" (via ready.txt) or timeout after 8 seconds
                start_time = time.time()
                while time.time() - start_time < 8:
                    if os.path.exists(ready_file):
                        # Add a tiny extra buffer so the user sees the Unity window appear
                        time.sleep(1.0) 
                        break
                    time.sleep(0.5)

            except Exception as e:
                # If launch fails, show error on the main thread
                self.controller.after(0, lambda: show_error("Launch Error", f"Failed to start: {e}"))
            
            finally:
                # Cleanup: Remove the files so they can't be reused
                for f in [auth_file, ready_file]:
                    if os.path.exists(f):
                        try: os.remove(f)
                        except: pass
                
                # Close the loading window safely on the main thread
                self.controller.after(0, loading_win.destroy)

        # Start the thread
        threading.Thread(target=launch_and_monitor, daemon=True).start()