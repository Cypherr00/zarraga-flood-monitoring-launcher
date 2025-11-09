# navigation.py
def go_to_page(controller, page_class):
    """
    Public helper used by UI code to switch pages.

    This simply delegates to the controller's page management API (e.g. MainFrame.show_page)
    to avoid duplicating page lookup logic and to prevent circular imports.
    """
    # prefer controller.show_page if available
    if hasattr(controller, "show_page"):
        try:
            controller.show_page(page_class)
            return
        except Exception:
            # fall back to manual lookup
            pass

    page = getattr(controller, "pages", {}).get(page_class)
    if page:
        page.tkraise()
    else:
        name = getattr(page_class, "__name__", str(page_class))
        print(f"Page {name} not found on controller.")


def go_back(controller):
    """
    Go back to a sensible default page. The app currently doesn't track history,
    so this will return to the main menu by name.
    """
    if hasattr(controller, "show_page_from_name"):
        controller.show_page_from_name("MainMenuPage")
    else:
        # best-effort fallback
        if hasattr(controller, "show_page"):
            # attempt to import MainMenuPage lazily
            try:
                from mainMenu import MainMenuPage

                controller.show_page(MainMenuPage)
                return
            except Exception:
                pass
        print("Cannot navigate back: controller lacks a show_page() API.")


def go_to_main_menu(controller):
    """Convenience wrapper to open the main menu."""
    if hasattr(controller, "show_page_from_name"):
        controller.show_page_from_name("MainMenuPage")
    else:
        go_back(controller)


def go_to_manage_accounts(controller):
    """Open the Account Manager page by name (avoids imports/circularities)."""
    if hasattr(controller, "show_page_from_name"):
        controller.show_page_from_name("AccountManagerPage")
    else:
        # last resort: try to import and use show_page
        try:
            from system_pages.manageAdminAccounts import AccountManagerPage

            go_to_page(controller, AccountManagerPage)
        except Exception:
            print("Unable to open AccountManagerPage")


def go_to_create_accounts(controller):
    """Open the CreateAccounts page by name."""
    if hasattr(controller, "show_page_from_name"):
        controller.show_page_from_name("CreateAccountsPage")
    else:
        try:
            from system_pages.account_modifications.createAccounts import CreateAccountsPage

            go_to_page(controller, CreateAccountsPage)
        except Exception:
            print("Unable to open CreateAccountsPage")
            
def back_to_main(controller):
        if hasattr(controller, "show_page_from_name"):
            controller.show_page_from_name("MainMenuPage")
        else:
            # fallback: try to import MainMenuPage and show it
            try:
                from mainMenu import MainMenuPage

                controller.show_page(MainMenuPage)
            except Exception:
                print("Unable to navigate back to main menu")
