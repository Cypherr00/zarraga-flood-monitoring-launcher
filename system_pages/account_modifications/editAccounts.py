import customtkinter as ctk
from utils.dialogs import show_info, show_error, ask_confirm
from utils.ui_styles import COLORS

class EditAccountsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(width=800, height=500, corner_radius=20, fg_color=COLORS["background"])

        # Title
        ctk.CTkLabel(
            self, text="Manage Accounts",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=10)

        # Main two-column layout
        content_frame = ctk.CTkFrame(self, fg_color="#1a1a1a")
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        content_frame.columnconfigure(0, weight=2)
        content_frame.columnconfigure(1, weight=1)

        # Left: account list with search bar
        left_frame = ctk.CTkFrame(content_frame, fg_color="#2b2b2b", corner_radius=10)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        header_frame = ctk.CTkFrame(left_frame, fg_color="#2b2b2b")
        header_frame.pack(fill="x", padx=10, pady=(10, 5))

        ctk.CTkLabel(
            header_frame, text="Accounts", font=ctk.CTkFont(size=18, weight="bold")
        ).pack(side="left", pady=5)

        # Search bar
        self.search_entry = ctk.CTkEntry(header_frame, placeholder_text="Search by username", width=160)
        self.search_entry.pack(side="left", padx=10)
        ctk.CTkButton(header_frame, text="Search", width=70, command=self.search_accounts).pack(side="left")

        # Scrollable list area
        self.scroll_frame = ctk.CTkScrollableFrame(left_frame, fg_color="#2b2b2b")
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Right: edit form
        edit_frame = ctk.CTkFrame(content_frame, fg_color="#222", corner_radius=10)
        edit_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=5)
        edit_frame.columnconfigure(0, weight=1)
        edit_frame.columnconfigure(1, weight=2)

        ctk.CTkLabel(edit_frame, text="Edit Account", font=ctk.CTkFont(size=18, weight="bold")).grid(
            row=0, column=0, columnspan=2, pady=(15, 10)
        )

        # Form fields with spacing
        ctk.CTkLabel(edit_frame, text="Account ID:").grid(row=1, column=0, sticky="e", padx=10, pady=10)
        self.entry_id = ctk.CTkEntry(edit_frame, width=180, state="disabled", justify="center")
        self.entry_id.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        ctk.CTkLabel(edit_frame, text="Username:").grid(row=2, column=0, sticky="e", padx=10, pady=10)
        self.entry_username = ctk.CTkEntry(edit_frame, width=180, justify="center")
        self.entry_username.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        ctk.CTkLabel(edit_frame, text="PIN (4 digits):").grid(row=3, column=0, sticky="e", padx=10, pady=10)
        self.entry_pin = ctk.CTkEntry(edit_frame, width=180, justify="center")
        self.entry_pin.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        ctk.CTkButton(edit_frame, text="Update Account", width=200, command=self.update_account).grid(
            row=4, column=0, columnspan=2, pady=20
        )

        # Back button
        ctk.CTkButton(
            self, text="Back",
            fg_color="#34495e", hover_color="#2c3e50",
            command=lambda: controller.show_page_from_name("AccountManagerPage")
        ).pack(pady=(0, 10))

        self.accounts = []
        self.load_accounts()

    def load_accounts(self, query=None):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        try:
            response = self.controller.supabase.table("user").select("*").execute()
            if not response.data:
                ctk.CTkLabel(self.scroll_frame, text="No accounts found.", text_color="gray").pack(pady=10)
                return

            # Filter search results if query present
            self.accounts = [
                acc for acc in response.data
                if not query or query.lower() in acc["user_name"].lower()
            ]

            if not self.accounts:
                ctk.CTkLabel(self.scroll_frame, text="No matching accounts.", text_color="gray").pack(pady=10)
                return

            for account in self.accounts:
                card = ctk.CTkFrame(self.scroll_frame, fg_color="#333", corner_radius=10)
                card.pack(fill="x", pady=6, padx=5, ipady=10)

                ctk.CTkLabel(
                    card, text=f"ID: {account['id']}", anchor="w", font=ctk.CTkFont(size=14)
                ).pack(anchor="w", padx=15, pady=(0, 2))
                ctk.CTkLabel(
                    card, text=f"Username: {account['user_name']}", anchor="w", font=ctk.CTkFont(size=16, weight="bold")
                ).pack(anchor="w", padx=15, pady=(0, 10))

                ctk.CTkButton(
                    card, text="Edit Account",
                    width=120, height=30,
                    fg_color="#27ae60", hover_color="#1e8449",
                    command=lambda acc=account: self.load_account_for_edit(acc)
                ).pack(anchor="center", pady=(0, 5))
        except Exception as e:
            show_error("Database Error", str(e))

    def search_accounts(self):
        query = self.search_entry.get().strip()
        self.load_accounts(query=query)

    def load_account_for_edit(self, account):
        self.entry_id.configure(state="normal")
        self.entry_id.delete(0, "end")
        self.entry_id.insert(0, account["id"])
        self.entry_id.configure(state="disabled")

        self.entry_username.delete(0, "end")
        self.entry_username.insert(0, account["user_name"])

        self.entry_pin.delete(0, "end")
        self.entry_pin.insert(0, account["pin"])

    def update_account(self):
        account_id = self.entry_id.get().strip()
        username = self.entry_username.get().strip()
        pin = self.entry_pin.get().strip()

        if not account_id or not username or not pin:
            show_error("Missing Fields", "All fields are required.")
            return
        if not pin.isdigit() or len(pin) != 4:
            show_error("Invalid PIN", "PIN must be exactly 4 digits.")
            return
        if not ask_confirm("Confirm Update", f"Update account '{username}' (ID: {account_id})?"):
            return

        try:
            response = self.controller.supabase.table("user").update({
                "user_name": username,
                "pin": pin
            }).eq("id", account_id).execute()

            if response.data:
                show_info("Success", "Account updated successfully.")
                self.load_accounts()
            else:
                show_error("Not Found", "Account could not be found or updated.")
        except Exception as e:
            show_error("Database Error", str(e))
