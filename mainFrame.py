# mainframe.py
import customtkinter as ctk
from supabase_init import init_supabase
from PIL import Image

from mainMenu import MainMenuPage
from system_pages.manageAdminAccounts import AccountManagerPage
from system_pages.account_modifications.createAccounts import CreateAccountsPage
from system_pages.account_modifications.editAccounts import EditAccountsPage
from system_pages.systemSettings import SystemSettingsPage
from system_pages.admin_account_management.adminCreateAccount import AdminCreateAccountPage
from system_pages.admin_account_management.adminConfigureAccount import adminConfigureAccountsPage
from loginPage import LoginPage

import sys
import os

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


# ---------------------------------------------------------
# Resource Path Helper (unchanged)
# ---------------------------------------------------------
def resource_path(relative_path: str) -> str:
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# ---------------------------------------------------------
# MainFrame Class (Fully Recreated)
# ---------------------------------------------------------
class MainFrame(ctk.CTk):
    def __init__(self):
        super().__init__()

        # -------------------------------------------------
        # Initialize Supabase
        # -------------------------------------------------
        self.supabase = init_supabase()

        # -------------------------------------------------
        # Window configuration
        # -------------------------------------------------
        self.title("Zarraga Flood Monitoring Main Menu")
        window_width, window_height = 900, 550

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.resizable(False, False)

        # -------------------------------------------------
        # Background Image (darkened)
        # -------------------------------------------------
        img_path = resource_path("assets/jalaur.png")
        original_img = Image.open(img_path).resize((window_width, window_height))

        dark_overlay = Image.new("RGBA", original_img.size, (0, 0, 0, 150))
        dark_img = Image.alpha_composite(original_img.convert("RGBA"), dark_overlay)

        self.bg_image = ctk.CTkImage(
            light_image=dark_img,
            dark_image=dark_img,
            size=(window_width, window_height)
        )

        bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # -------------------------------------------------
        # RIGHT-SIDE FIXED IMAGE PANEL  (NEW)
        # -------------------------------------------------
        right_img_path = resource_path("assets/wide-logo.jfif")

        self.right_side_image = ctk.CTkImage(
            light_image=Image.open(right_img_path),
            size=(300, 300)     # <--- adjustable
        )

        self.right_panel = ctk.CTkLabel(
            self,
            image=self.right_side_image,
            text="",
            fg_color="transparent"
        )

        # Always visible, fixed on the right
        self.right_panel.place(
            relx=1.0, rely=0.5,
            anchor="e",
            x=-50
        )

        # -------------------------------------------------
        # CENTER/LEFT PAGE CONTAINER (for all pages)
        # -------------------------------------------------
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # -------------------------------------------------
        # Page Registration
        # -------------------------------------------------
        self.pages = {
            MainMenuPage: MainMenuPage(self.container, self, account_page_class=AccountManagerPage),
            AccountManagerPage: AccountManagerPage(self.container, self),
            CreateAccountsPage: CreateAccountsPage(self.container, self),
            EditAccountsPage: EditAccountsPage(self.container, self),
            SystemSettingsPage: SystemSettingsPage(
                self.container,
                self,
                admin_create_account_page=AdminCreateAccountPage,
                admin_configure_account_page=adminConfigureAccountsPage
            ),
            AdminCreateAccountPage: AdminCreateAccountPage(self.container, self),
            adminConfigureAccountsPage: adminConfigureAccountsPage(self.container, self),
            LoginPage: LoginPage(self.container, self),
        }

        # Hide all pages initially
        for page in self.pages.values():
            page.grid(row=0, column=0, sticky="nsew")
            page.grid_remove()

        # Default page
        self.after(0, lambda: self.show_page(LoginPage))


    # ---------------------------------------------------------
    # Optional helper: Replace right-side image anytime
    # ---------------------------------------------------------
    def set_right_panel_image(self, relative_path: str, size=(260, 260)):
        new_img = ctk.CTkImage(
            light_image=Image.open(resource_path(relative_path)),
            size=size
        )
        self.right_side_image = new_img
        self.right_panel.configure(image=new_img)


    # ---------------------------------------------------------
    # Connection Test (unchanged)
    # ---------------------------------------------------------
    def _test_connection(self) -> bool:
        try:
            self.supabase.table("user").select("user_name").limit(1).execute()
            return True
        except Exception:
            return False


    # ---------------------------------------------------------
    # show_page (your exact logic retained)
    # ---------------------------------------------------------
    def show_page(self, page_identifier):
        # Resolve string to class if needed
        if isinstance(page_identifier, str):
            page_class = None
            for cls in self.pages.keys():
                if cls.__name__ == page_identifier:
                    page_class = cls
                    break
            if not page_class:
                print(f"Page '{page_identifier}' not found.")
                return
        else:
            page_class = page_identifier

        # Hide all
        for page in self.pages.values():
            page.grid_remove()

        # Adjust container alignment
        if page_class.__name__ in ("LoginPage", "MainMenuPage", "AccountManagerPage"):
            self.container.place(relx=0.0, rely=0.5, anchor="w")
        else:
            self.container.place(relx=0.5, rely=0.5, anchor="center")

        # Show requested page
        page = self.pages.get(page_class)
        if page:
            page.grid()
            page.tkraise()
        else:
            print(f"Page {page_class.__name__} not found.")
