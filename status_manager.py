import json
import os

STATUS_FILE = "bot_status.json"

def load_status():
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "r") as f:
            return json.load(f)
    return {
        "bot_running": False,
        "watching": False,
        "points": 0,
        "start_timestamp": 0
    }

def save_status(bot_running, watching, points, start_timestamp):
    with open(STATUS_FILE, "w") as f:
        json.dump({
            "bot_running": bot_running,
            "watching": watching,
            "points": points,
            "start_timestamp": start_timestamp
        }, f)
