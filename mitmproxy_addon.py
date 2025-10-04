import json
import asyncio
import logging
from threading import Thread

from mitmproxy import http
from mitmproxy.tools.dump import DumpMaster
from mitmproxy.options import Options

from config import MITMPROXY_LISTEN_HOST, MITMPROXY_LISTEN_PORT

logger = logging.getLogger(__name__)

mitmproxy_master = None
mitmproxy_addon_instance = None

class NameSpoofAddon:
    def __init__(self, new_name):
        self.new_name = new_name
        logger.debug(f"Addon initialized with spoof name '{self.new_name}'")

    def update_name(self, new_name):
        logger.info(f"Updating spoof name: {self.new_name} -> {new_name}")
        self.new_name = new_name

    def response(self, flow: http.HTTPFlow):
        target_domains = ["epicgames.dev", "epicgames.com", "psyonix.com", "live.psynet.gg"]
        if any(d in flow.request.pretty_host for d in target_domains):
            if "application/json" in flow.response.headers.get("Content-Type", ""):
                self._process_json_body(flow)

    def _process_json_body(self, flow: http.HTTPFlow):
        try:
            body_data = flow.response.json()
        except json.JSONDecodeError:
            return

        if isinstance(body_data, list) and body_data and isinstance(body_data[0], dict):
            user_data = body_data[0]
            if "displayName" in user_data:
                old_name = user_data["displayName"]
                if old_name != self.new_name:
                    user_data["displayName"] = self.new_name
                    flow.response.content = json.dumps(body_data, ensure_ascii=False).encode("utf-8")
                    flow.response.headers["Content-Length"] = str(len(flow.response.content))
                    logger.info(f"Name spoofed: {old_name} -> {self.new_name}")

def run_mitmproxy_thread_target(new_name, gui_root):
    global mitmproxy_master, mitmproxy_addon_instance
    logger.debug("Starting mitmproxy thread ...")

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def run_proxy_async():
        nonlocal new_name
        try:
            options = Options(listen_host=MITMPROXY_LISTEN_HOST, listen_port=MITMPROXY_LISTEN_PORT, mode=["regular"])
            mitmproxy_master = DumpMaster(options, with_termlog=False)
            mitmproxy_addon_instance = NameSpoofAddon(new_name)
            mitmproxy_master.addons.add(mitmproxy_addon_instance)
            logger.info(f"Proxy running at {MITMPROXY_LISTEN_HOST}:{MITMPROXY_LISTEN_PORT}")
            await mitmproxy_master.run()
        except Exception as e:
            logger.error(f"Mitmproxy runtime error: {e}")
            from tkinter import messagebox
            gui_root.after(0, lambda: messagebox.showerror("Mitmproxy Error", str(e)))
        finally:
            logger.debug("mitmproxy shutting down.")
            if mitmproxy_master:
                mitmproxy_master.shutdown()

    try:
        asyncio.run(run_proxy_async())
    except Exception as e:
        logger.error(f"Proxy async loop error: {e}")

def stop_mitmproxy_gracefully():
    global mitmproxy_master
    logger.debug("Stopping mitmproxy ...")
    if mitmproxy_master:
        mitmproxy_master.shutdown()
