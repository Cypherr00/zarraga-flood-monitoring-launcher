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

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MainFrame(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Initialize Supabase client
        self.supabase = init_supabase()

        # Window configuration
        self.title("Zarraga Flood Monitoring Main Menu")
        window_width, window_height = 900, 550
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.resizable(False, False)

        # Load and darken background image
        img_path = "assets/zarraga-dailyGuardian.jpg"  # adjust if path differs
        original_img = Image.open(img_path).resize((window_width, window_height))
        dark_overlay = Image.new("RGBA", original_img.size, (0, 0, 0, 150))
        dark_img = Image.alpha_composite(original_img.convert("RGBA"), dark_overlay)

        # Use CTkImage for proper scaling and DPI support
        self.bg_image = ctk.CTkImage(
            light_image=dark_img,
            dark_image=dark_img,
            size=(window_width, window_height)
        )

        # Background label
        bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Page container
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        # Page registration
        self.pages = {
            MainMenuPage: MainMenuPage(self.container, self, account_page_class=AccountManagerPage),
            AccountManagerPage: AccountManagerPage(self.container, self),
            CreateAccountsPage: CreateAccountsPage(self.container, self),
            EditAccountsPage: EditAccountsPage(self.container, self),
            SystemSettingsPage: SystemSettingsPage(
                self.container,
                self,
                admin_create_account_page=AdminCreateAccountPage,
                admin_configure_account_page=adminConfigureAccountsPage,
            ),
            AdminCreateAccountPage: AdminCreateAccountPage(self.container, self),
            adminConfigureAccountsPage: adminConfigureAccountsPage(self.container, self),
            LoginPage: LoginPage(self.container, self),
        }

        for page in self.pages.values():
            page.grid(row=0, column=0, sticky="nsew")

        # Show initial page after initialization
        self.after(0, lambda: self.show_page(LoginPage))

        # Status bar
        self.status_bar = ctk.CTkLabel(
            self,
            text=f"Database: Connected" if self._test_connection() else "Database: Disconnected",
            anchor="w",
            font=ctk.CTkFont(size=12),
            text_color="#7f8c8d",
            fg_color="transparent",
        )
        self.status_bar.pack(side="bottom", fill="x", padx=10, pady=8)

    def _test_connection(self) -> bool:
        try:
            self.supabase.table("user").select("user_name").limit(1).execute()
            return True
        except Exception:
            return False

    def show_page(self, page_class):
        page = self.pages.get(page_class)
        if page:
            page.tkraise()
        else:
            print(f"Page {getattr(page_class, '__name__', str(page_class))} not found.")

    def show_page_from_name(self, page_name: str):
        for page_class in self.pages:
            if page_class.__name__ == page_name:
                self.show_page(page_class)
                return
        print(f"Page '{page_name}' not found in registry.")
