import sys
import logging
from tkinter import messagebox

import customtkinter as ctk

from config import APP_NAME, APP_VERSION
from logger_setup import setup_logging
from gui import SpooferGUI

def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger = logging.getLogger(__name__)
    logger.critical("Unhandled Exception", exc_info=(exc_type, exc_value, exc_traceback))
    messagebox.showerror(
        "Application Error",
        f"An unexpected error occurred:\n\n{exc_value}\n\n"
        f"Details have been written to the log file.\n"
        f"Please restart the application. If the problem persists, share the log file.",
    )

def main():
    setup_logging()
    logger = logging.getLogger(__name__)
    
    sys.excepthook = handle_exception

    try:
        from mitmproxy import http
        from mitmproxy.tools.dump import DumpMaster
        from mitmproxy.options import Options
        logger.debug("mitmproxy modules imported successfully.")
    except ImportError as e:
        logger.critical(f"Failed to import mitmproxy modules: {e}")
        messagebox.showerror("Import Error", f"Failed to import mitmproxy components.\nError: {e}")
        return
    except Exception as e:
        logger.critical(f"Unexpected error during mitmproxy import: {e}")
        messagebox.showerror("Startup Error", f"Unexpected startup error: {e}")
        return

    logger.info(f"{APP_NAME} v{APP_VERSION} starting ...")
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    root = ctk.CTk()
    root.configure(fg_color="#01024D")  # Set main window background to match theme
    
    try:
        import ctypes
        from ctypes import wintypes
        hwnd = root.winfo_id()
        gold_color = 0x004C9FBD
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd, 35, ctypes.byref(ctypes.c_int(gold_color)), 4
        )
    except Exception as e:
        logger.warning(f"Could not set title bar color: {e}")
    
    app = SpooferGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
    logger.info("Application exited cleanly.")

if __name__ == "__main__":
    main()
