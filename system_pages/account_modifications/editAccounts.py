import customtkinter as ctk
from utils.dialogs import show_info, show_error, ask_confirm
from utils.ui_styles import COLORS

class EditAccountsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.current_is_active = True
        
        self.configure(width=800, height=500, corner_radius=0, fg_color=COLORS["background"])
        self.pack_propagate(False)

        # THE FIX (Part 1): Automatically refresh data whenever this frame is shown on screen
        self.bind("<Map>", self._on_map)

        # =========================================
        # TOP HEADER
        # =========================================
        top_bar = ctk.CTkFrame(self, fg_color="transparent")
        top_bar.pack(fill="x", padx=20, pady=(15, 5))

        ctk.CTkButton(
            top_bar, text="◄ Back", width=80,
            fg_color="transparent", hover_color=COLORS["secondary"],
            text_color=COLORS["text"], font=ctk.CTkFont(size=14, weight="bold"),
            command=lambda: self.controller.show_page("AccountManagerPage")
        ).pack(side="left")

        ctk.CTkLabel(
            top_bar, text="Manage Accounts",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=COLORS["text"]
        ).pack(side="left", padx=20)

        # =========================================
        # MAIN LAYOUT
        # =========================================
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        content_frame.rowconfigure(0, weight=1) 
        content_frame.columnconfigure(0, weight=5) 
        content_frame.columnconfigure(1, weight=4) 

        # -----------------------------------------
        # LEFT COLUMN: Search & List
        # -----------------------------------------
        left_frame = ctk.CTkFrame(content_frame, fg_color=COLORS["secondary"], corner_radius=12)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        search_header = ctk.CTkFrame(left_frame, fg_color="transparent")
        search_header.pack(fill="x", padx=15, pady=(15, 10))

        self.search_entry = ctk.CTkEntry(
            search_header, placeholder_text="Search by username...", 
            fg_color="white", text_color=COLORS["text"]
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.search_entry.bind("<Return>", lambda event: self.search_accounts())

        ctk.CTkButton(
            search_header, text="Search", width=70,
            fg_color=COLORS["button"], hover_color=COLORS["button_hover"],
            command=self.search_accounts
        ).pack(side="left")

        # THE FIX (Part 2): Added a manual Refresh button for better UX
        ctk.CTkButton(
            search_header, text="↻", width=40,
            fg_color="transparent", border_width=2, border_color=COLORS["button"],
            hover_color=COLORS["secondary"], text_color=COLORS["text"],
            command=lambda: self.load_accounts()
        ).pack(side="left", padx=(10, 0))

        self.scroll_frame = ctk.CTkScrollableFrame(left_frame, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # -----------------------------------------
        # RIGHT COLUMN: Edit Form
        # -----------------------------------------
        edit_frame = ctk.CTkFrame(content_frame, fg_color="white", corner_radius=12)
        edit_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        edit_frame.columnconfigure(0, weight=1)
        edit_frame.columnconfigure(1, weight=2)
        
        edit_frame.rowconfigure(5, weight=1)

        ctk.CTkLabel(
            edit_frame, text="Account Details", 
            font=ctk.CTkFont(size=18, weight="bold"), text_color=COLORS["text"]
        ).grid(row=0, column=0, columnspan=2, pady=(20, 15))

        lbl_font = ctk.CTkFont(size=14)
        entry_kwargs = {"width": 200, "fg_color": COLORS["secondary"], "text_color": COLORS["text"], "justify": "center"}

        ctk.CTkLabel(edit_frame, text="Account ID:", font=lbl_font, text_color=COLORS["text"]).grid(row=1, column=0, sticky="e", padx=10, pady=10)
        self.entry_id = ctk.CTkEntry(edit_frame, state="disabled", **entry_kwargs)
        self.entry_id.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        ctk.CTkLabel(edit_frame, text="Username:", font=lbl_font, text_color=COLORS["text"]).grid(row=2, column=0, sticky="e", padx=10, pady=10)
        self.entry_username = ctk.CTkEntry(edit_frame, **entry_kwargs)
        self.entry_username.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        ctk.CTkLabel(edit_frame, text="PIN (4 digits):", font=lbl_font, text_color=COLORS["text"]).grid(row=3, column=0, sticky="e", padx=10, pady=10)
        self.entry_pin = ctk.CTkEntry(edit_frame, **entry_kwargs)
        self.entry_pin.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        btn_frame = ctk.CTkFrame(edit_frame, fg_color="transparent")
        btn_frame.grid(row=4, column=0, columnspan=2, pady=(30, 20))

        ctk.CTkButton(
            btn_frame, text="Update", width=110,
            fg_color=COLORS["button"], hover_color=COLORS["button_hover"],
            command=self.update_account
        ).pack(side="left", padx=10)

        self.btn_status = ctk.CTkButton(
            btn_frame, text="Deactivate", width=110,
            fg_color=COLORS["danger"], hover_color=COLORS.get("danger_hover", "#c82333"),
            command=self.toggle_account_status
        )
        self.btn_status.pack(side="left", padx=10)

        self.accounts = []
        self.load_accounts()

    # =========================================
    # CORE LOGIC
    # =========================================
    def _on_map(self, event):
        """Triggered automatically when the frame is drawn on screen."""
        # We check if the widget triggering the event is THIS frame to prevent child widgets 
        # (like buttons or entries) from accidentally triggering a database refresh when clicked.
        if event.widget == self:
            self.load_accounts()

    def clear_form(self):
        """Wipes the form clean and resets the dynamic button."""
        self.entry_id.configure(state="normal")
        self.entry_id.delete(0, "end")
        self.entry_id.configure(state="disabled")
        
        self.entry_username.delete(0, "end")
        self.entry_pin.delete(0, "end")
        
        self.current_is_active = True
        self.btn_status.configure(
            text="Deactivate", 
            fg_color=COLORS["danger"], 
            hover_color=COLORS.get("danger_hover", "#c82333")
        )

    def load_accounts(self, query=None):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        try:
            response = self.controller.supabase.table("user").select("*").execute()
            if not response.data:
                ctk.CTkLabel(self.scroll_frame, text="No accounts found.", text_color=COLORS["subtext"]).pack(pady=20)
                return

            self.accounts = [
                acc for acc in response.data
                if not query or query.lower() in acc["user_name"].lower()
            ]

            if not self.accounts:
                ctk.CTkLabel(self.scroll_frame, text="No matching accounts.", text_color=COLORS["subtext"]).pack(pady=20)
                return

            self.accounts.sort(key=lambda x: x.get("id", 0))

            for account in self.accounts:
                card = ctk.CTkFrame(self.scroll_frame, fg_color="white", corner_radius=8)
                card.pack(fill="x", pady=5, padx=5)

                is_active = account.get("is_active", True)
                
                display_name = account['user_name']
                name_color = COLORS["text"]
                if not is_active:
                    display_name += " (Inactive)"
                    name_color = COLORS["subtext"] 

                info_frame = ctk.CTkFrame(card, fg_color="transparent")
                info_frame.pack(side="left", fill="x", expand=True, padx=15, pady=10)
                
                ctk.CTkLabel(
                    info_frame, 
                    text=display_name, 
                    font=ctk.CTkFont(size=14, weight="bold"), 
                    text_color=name_color,
                    anchor="w"
                ).pack(fill="x")

                ctk.CTkButton(
                    card, text="Edit", width=60, height=28,
                    fg_color=COLORS["button"], hover_color=COLORS["button_hover"],
                    command=lambda acc=account: self.load_account_for_edit(acc)
                ).pack(side="right", padx=15, pady=10)

        except Exception as e:
            show_error("Database Error", f"Unable to connect to the database.\n{e}")

    def search_accounts(self):
        query = self.search_entry.get().strip()
        self.load_accounts(query=query)

    def load_account_for_edit(self, account):
        self.clear_form() 
        
        self.entry_id.configure(state="normal")
        self.entry_id.insert(0, account["id"])
        self.entry_id.configure(state="disabled")

        self.entry_username.insert(0, account["user_name"])
        self.entry_pin.insert(0, account["pin"])
        
        self.current_is_active = account.get("is_active", True)
        if self.current_is_active:
            self.btn_status.configure(
                text="Deactivate", 
                fg_color=COLORS["danger"], 
                hover_color=COLORS.get("danger_hover", "#c82333")
            )
        else:
            self.btn_status.configure(
                text="Reactivate", 
                fg_color=COLORS.get("success", "#28a745"), 
                hover_color=COLORS.get("success_hover", "#218838")
            )

    def update_account(self):
        account_id = self.entry_id.get().strip()
        username = self.entry_username.get().strip()
        pin = self.entry_pin.get().strip()

        if not account_id:
            show_error("No Selection", "Please select an account to edit first.")
            return
        if not username or not pin:
            show_error("Missing Fields", "Username and PIN are required.")
            return
        if not pin.isdigit() or len(pin) != 4:
            show_error("Invalid PIN", "PIN must be exactly 4 digits.")
            return
            
        if not ask_confirm("Confirm Update", f"Update account '{username}'?"):
            return

        try:
            response = self.controller.supabase.table("user").update({
                "user_name": username,
                "pin": pin
            }).eq("id", account_id).execute()

            if response.data:
                show_info("Success", "Account updated successfully.")
                self.clear_form()
                self.load_accounts()
            else:
                show_error("Not Found", "Account could not be updated.")
        except Exception as e:
            show_error("Database Error", f"Unable to update account.\n{e}")

    def toggle_account_status(self):
        account_id = self.entry_id.get().strip()
        username = self.entry_username.get().strip()

        if not account_id:
            show_error("No Selection", "Please select an account first.")
            return

        action_name = "Deactivate" if self.current_is_active else "Reactivate"
        
        prompt = f"Are you sure you want to {action_name.lower()} '{username}'?\n\n"
        if self.current_is_active:
            prompt += "They will no longer be able to log in."
        else:
            prompt += "Their access will be fully restored."

        if not ask_confirm(f"Confirm {action_name}", prompt):
            return

        try:
            new_status = not self.current_is_active 
            
            response = self.controller.supabase.table("user").update({
                "is_active": new_status
            }).eq("id", account_id).execute()
            
            if response.data:
                show_info(action_name, f"Account '{username}' has been successfully {action_name.lower()}d.")
                self.clear_form()
                self.load_accounts()
            else:
                show_error("Error", f"Could not {action_name.lower()} the account.")
                
        except Exception as e:
            show_error("Database Error", f"Failed to change account status.\n\nReason: {str(e)}")