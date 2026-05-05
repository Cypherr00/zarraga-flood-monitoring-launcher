import customtkinter as ctk
from navigation import back_to_main
from utils.ui_styles import COLORS

class AccountManagerPage(ctk.CTkFrame):
    def __init__(self, parent, controller, main_page_class=None):
        super().__init__(parent)
        self.controller = controller
        self.main_page_class = main_page_class
        
        # RESTORED: Your exact original main menu dimensions and corner radius
        self.configure(width=300, height=550, fg_color=COLORS["background"], corner_radius=20)
        self.pack_propagate(False) 

        # Create a container frame to hold everything and perfectly center it vertically
        menu_container = ctk.CTkFrame(self, fg_color="transparent")
        menu_container.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        ctk.CTkLabel(
            menu_container, text="Account Management",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COLORS["text"],
            wraplength=260 # Added wrapping so it fits cleanly inside the 300px width
        ).pack(pady=(0, 10))

        # Subtitle
        ctk.CTkLabel(
            menu_container,
            text="Create and manage user accounts for the mobile app.",
            font=ctk.CTkFont(size=14),
            text_color=COLORS.get("subtext", "gray"), 
            wraplength=260,
            justify="center"
        ).pack(pady=(0, 20))

        # Divider (Uses secondary color, adjusted width to 260 to fit frame)
        ctk.CTkFrame(
            menu_container, height=2, width=260, 
            fg_color=COLORS["secondary"]
        ).pack(pady=(0, 30))

        # Buttons - Taller for modern feel, widths kept at 240 to fit perfectly inside 300
        ctk.CTkButton(
            menu_container, text="Create New Account", 
            width=240, height=45,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=COLORS["button"], hover_color=COLORS["button_hover"],
            command=lambda: controller.show_page("CreateAccountsPage")
        ).pack(pady=10)

        ctk.CTkButton(
            menu_container, text="View / Edit Accounts", 
            width=240, height=45,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=COLORS["button"], hover_color=COLORS["button_hover"],
            command=lambda: controller.show_page("EditAccountsPage")
        ).pack(pady=10)

        # Back Button - Styled as a subtle outlined button
        ctk.CTkButton(
            menu_container, text="Back to Main Menu", 
            width=240, height=45,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="transparent", hover_color=COLORS["secondary"],
            border_width=2, border_color=COLORS["secondary"], text_color=COLORS["text"],
            command=lambda: back_to_main(self.controller)
        ).pack(pady=(30, 0))