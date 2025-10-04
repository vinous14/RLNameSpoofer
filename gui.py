import logging
from threading import Thread, Event
from tkinter import messagebox
import os
import winreg
import sys

import customtkinter as ctk
from PIL import Image

from config import load_config, save_config, MITMPROXY_LISTEN_HOST, MITMPROXY_LISTEN_PORT
from utils import is_port_in_use, set_system_proxy, disable_system_proxy
from mitmproxy_addon import run_mitmproxy_thread_target, stop_mitmproxy_gracefully

logger = logging.getLogger(__name__)

class SpooferGUI:
    def __init__(self, master):
        logger.info("Initializing GUI ...")
        self.master = master
        self.proxy_thread = None
        self.is_proxy_running = False
        self.auto_scan_var = ctk.BooleanVar(value=False)
        self.startup_var = ctk.BooleanVar(value=self._is_in_startup())
        self.auto_scan_stop_event = Event()
        self.rl_process_active = False
        self.app_config = load_config()
        self.new_name_var = ctk.StringVar(value=self.app_config["last_spoof_name"])
        self.auto_scan_var.set(self.app_config.get("auto_scan_on_startup", False))
        self._setup_window()
        self._create_widgets()
        self._bind_events()

    def _setup_window(self):
        logger.debug("Setting up main window ...")
        self.master.title("vinxzn's Name Spoofer")
        self.master.geometry("500x450")
        
        icon_path = os.path.join(os.path.dirname(__file__), "icon.png.ico")
        if os.path.exists(icon_path):
            try:
                self.master.iconbitmap(icon_path)
            except Exception as e:
                logger.warning(f"Could not set window icon: {e}")

    def _create_widgets(self):
        logger.debug("Creating widgets ...")
        main_frame = ctk.CTkFrame(self.master, fg_color="#01024D", corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=0, pady=0)

        header_frame = ctk.CTkFrame(main_frame, fg_color="#01024D", height=80, corner_radius=0)
        header_frame.pack(fill="x", pady=(0, 1))
        header_frame.pack_propagate(False)

        icon_path = os.path.join(os.path.dirname(__file__), "icon.png.ico")
        if os.path.exists(icon_path):
            try:
                logo_image = ctk.CTkImage(
                    light_image=Image.open(icon_path),
                    dark_image=Image.open(icon_path),
                    size=(50, 50)
                )
                logo_label = ctk.CTkLabel(header_frame, image=logo_image, text="")
                logo_label.pack(side="left", padx=15, pady=15)
            except Exception as e:
                logger.warning(f"Could not load logo image: {e}")
                logo_label = ctk.CTkLabel(header_frame, text="🚀", font=ctk.CTkFont(size=40))
                logo_label.pack(side="left", padx=15, pady=15)
        else:
            logo_label = ctk.CTkLabel(header_frame, text="🚀", font=ctk.CTkFont(size=40))
            logo_label.pack(side="left", padx=15, pady=15)

        title_label = ctk.CTkLabel(
            header_frame, 
            text="vinxzn's Name Spoofer", 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#FFFFFF"
        )
        title_label.pack(side="left", padx=(10, 0), pady=15)

        content_frame = ctk.CTkFrame(main_frame, fg_color="#01024D", corner_radius=0)
        content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        input_label = ctk.CTkLabel(content_frame, text="Enter your desired name:", font=ctk.CTkFont(size=14), text_color="#FFFFFF")
        input_label.pack(pady=(20, 5))

        self.new_name_entry = ctk.CTkEntry(
            content_frame, 
            textvariable=self.new_name_var,
            font=ctk.CTkFont(size=14),
            height=35,
            fg_color="#01024D",
            text_color="#FFFFFF",
            placeholder_text="Enter name here..."
        )
        self.new_name_entry.pack(pady=5, padx=40, fill="x")

        self.toggle_button = ctk.CTkButton(
            content_frame, 
            text="ACTIVATE", 
            command=self.toggle_proxy_clicked,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=45,
            fg_color="#01024D",
            hover_color="#02032F",
            text_color="#FFFFFF"
        )
        self.toggle_button.pack(pady=20, padx=40, fill="x")

        self.auto_scan_checkbox = ctk.CTkCheckBox(
            content_frame, 
            text="Auto-attach to Rocket League", 
            variable=self.auto_scan_var,
            font=ctk.CTkFont(size=12),
            text_color="#FFFFFF",
            checkmark_color="#FFFFFF",
            fg_color="#01024D"
        )
        self.auto_scan_checkbox.pack(pady=5)

        self.startup_checkbox = ctk.CTkCheckBox(
            content_frame,
            text="Boot at startup",
            variable=self.startup_var,
            font=ctk.CTkFont(size=12),
            text_color="#FFFFFF",
            checkmark_color="#FFFFFF",
            fg_color="#01024D",
            command=self.on_startup_toggle
        )
        self.startup_checkbox.pack(pady=5)

        self.status_label = ctk.CTkLabel(
            content_frame, 
            text="Proxy: Inactive",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#FFFFFF"
        )
        self.status_label.pack(pady=(10, 10))

        watermark_label = ctk.CTkLabel(
            content_frame,
            text="Made by vinxzn",
            font=ctk.CTkFont(size=10),
            text_color="#808080"
        )
        watermark_label.pack(pady=(0, 20))

    def _bind_events(self):
        self.new_name_entry.bind("<KeyRelease>", self.on_name_entry_change)
        self.auto_scan_checkbox.configure(command=self.on_auto_scan_toggle)
        self.startup_checkbox.configure(command=self.on_startup_toggle)

    def on_name_entry_change(self, event):
        save_config({"last_spoof_name": self.new_name_var.get(), "auto_scan_on_startup": self.auto_scan_var.get()})
        logger.debug(f"Name entry changed: {self.new_name_var.get()}")

    def toggle_proxy_clicked(self):
        if not self.is_proxy_running:
            self.start_proxy()
        else:
            self.stop_proxy()

    def start_proxy(self):
        logger.info("Starting proxy ...")
        if is_port_in_use(MITMPROXY_LISTEN_HOST, MITMPROXY_LISTEN_PORT):
            messagebox.showerror("Port Error", "Port in use")
            return
        if not set_system_proxy(MITMPROXY_LISTEN_HOST, MITMPROXY_LISTEN_PORT):
            messagebox.showerror("Proxy Error", "Could not set system proxy")
            return
        self.proxy_thread = Thread(target=run_mitmproxy_thread_target, args=(self.new_name_var.get(), self.master), daemon=True)
        self.proxy_thread.start()
        self.is_proxy_running = True
        self.status_label.configure(text="Proxy: Active", text_color="#00FF00")
        self.toggle_button.configure(text="DEACTIVATE")

    def stop_proxy(self):
        logger.info("Stopping proxy ...")
        stop_mitmproxy_gracefully()
        disable_system_proxy()
        self.is_proxy_running = False
        self.status_label.configure(text="Proxy: Inactive", text_color="#FFFFFF")
        self.toggle_button.configure(text="ACTIVATE")

    def on_auto_scan_toggle(self):
        if self.auto_scan_var.get():
            logger.info("Auto-scan enabled.")
        else:
            logger.info("Auto-scan disabled.")

    def _is_in_startup(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run")
            try:
                value, _ = winreg.QueryValueEx(key, "vinxzn Name Spoofer")
                winreg.CloseKey(key)
                return True
            except FileNotFoundError:
                winreg.CloseKey(key)
                return False
        except Exception as e:
            logger.warning(f"Could not check startup status: {e}")
            return False

    def _add_to_startup(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
            exe_path = sys.executable
            script_path = os.path.abspath(__file__).replace("gui.py", "main.py")
            startup_command = f'"{exe_path}" "{script_path}"'
            winreg.SetValueEx(key, "vinxzn Name Spoofer", 0, winreg.REG_SZ, startup_command)
            winreg.CloseKey(key)
            logger.info("Added to startup successfully")
            return True
        except Exception as e:
            logger.error(f"Could not add to startup: {e}")
            messagebox.showerror("Startup Error", f"Could not add to startup: {e}")
            return False

    def _remove_from_startup(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
            winreg.DeleteValue(key, "vinxzn Name Spoofer")
            winreg.CloseKey(key)
            logger.info("Removed from startup successfully")
            return True
        except FileNotFoundError:
            logger.info("Entry not found in startup")
            return True
        except Exception as e:
            logger.error(f"Could not remove from startup: {e}")
            messagebox.showerror("Startup Error", f"Could not remove from startup: {e}")
            return False

    def on_startup_toggle(self):
        if self.startup_var.get():
            if self._add_to_startup():
                logger.info("Startup enabled.")
            else:
                self.startup_var.set(False)
        else:
            if self._remove_from_startup():
                logger.info("Startup disabled.")
            else:
                self.startup_var.set(True)

    def on_closing(self):
        logger.info("Closing application ...")
        if self.is_proxy_running:
            self.stop_proxy()
        self.master.destroy()