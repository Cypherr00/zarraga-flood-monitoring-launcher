# dialogs.py
import customtkinter as ctk
from tkinter import messagebox

def show_info(title: str, message: str):
    """
    Display an information message.
    Parameters:
    title (R): string shown in the popup title bar
    message (R): main text content of the info dialog
    """
    messagebox.showinfo(title, message)


def show_warning(title: str, message: str):
    """
    Display a warning message.
    Parameters:
    title (R): string shown in the popup title bar
    message (R): warning text to alert the user
    """
    messagebox.showwarning(title, message)


def show_error(title: str, message: str):
    """
    Display an error message.
    Parameters:
    title (R): string shown in the popup title bar
    message (R): error text explaining what went wrong
    """
    messagebox.showerror(title, message)


def ask_confirm(title: str, message: str) -> bool:
    """
    Display a confirmation dialog (Yes/No).
    Parameters:
    title (R): popup title text
    message (R): confirmation question
    Returns:
    bool: True if user clicks 'Yes', False otherwise
    """
    return messagebox.askyesno(title, message)


def ask_okcancel(title: str, message: str) -> bool:
    """
    Display a confirmation dialog (OK/Cancel).
    Parameters:
    title (R): popup title text
    message (R): message body
    Returns:
    bool: True if user clicks 'OK', False otherwise
    """
    return messagebox.askokcancel(title, message)
