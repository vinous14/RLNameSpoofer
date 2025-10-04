import os
import sys
import json
import logging

logger = logging.getLogger(__name__)

APP_NAME = "RLNameSpoofer"
APP_VERSION = "1.0.0"

if sys.platform == "win32":
    APP_DIR = os.path.join(os.getenv('APPDATA'), APP_NAME)
elif sys.platform == "darwin":
    APP_DIR = os.path.join(os.path.expanduser('~'), 'Library', 'Application Support', APP_NAME)
else:
    APP_DIR = os.path.join(os.path.expanduser('~'), '.config', APP_NAME)

os.makedirs(APP_DIR, exist_ok=True)

CONFIG_FILE_NAME = "config.json"
CONFIG_FILE_PATH = os.path.join(APP_DIR, CONFIG_FILE_NAME)
LOG_FILE = os.path.join(APP_DIR, "mitmproxy_app_log.txt")

DEFAULT_CONFIG = {
    "last_spoof_name": "vinxzn likes men!",
    "auto_scan_on_startup": False,
}

MITMPROXY_LISTEN_HOST = "127.0.0.1"
MITMPROXY_LISTEN_PORT = 8080
ROCKET_LEAGUE_PROCESS_NAME = "RocketLeague.exe"
SCAN_INTERVAL_SECONDS = 0.5
MAX_NAME_LENGTH = 32

def get_asset_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

def load_config():
    logger.debug("Loading config.json ...")
    if os.path.exists(CONFIG_FILE_PATH):
        try:
            with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as f:
                config = json.load(f)
                logger.info("Config loaded successfully.")
                return {**DEFAULT_CONFIG, **config}
        except json.JSONDecodeError as e:
            logger.error(f"Config file corrupted: {e}. Using defaults.")
            return DEFAULT_CONFIG
        except Exception as e:
            logger.error(f"Unexpected error loading config: {e}. Using defaults.")
            return DEFAULT_CONFIG
    else:
        logger.warning("Config file not found. Using defaults.")
        return DEFAULT_CONFIG

def save_config(config):
    logger.debug("Saving config.json ...")
    try:
        with open(CONFIG_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        logger.info("Config saved successfully.")
    except Exception as e:
        logger.error(f"Failed to save config: {e}")
