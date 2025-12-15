"""Application entry point with database encryption handling."""

import os

from src.database import decrypt_database

# Use environment variable flag to prevent re-entry when NiceGUI re-runs main.py
if __name__ == "__main__" and not os.environ.get("_NICEGUI_STARTED"):
    os.environ["_NICEGUI_STARTED"] = "1"
    decrypt_database()

# Import GUI module (workers need this for __mp_main__)
from gui.gui_app import run_app

if __name__ in {"__main__", "__mp_main__"}:
    run_app()
