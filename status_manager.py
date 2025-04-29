import json
import os

STATUS_FILE = "bot_status.json"

def load_status():
    if not os.path.exists(STATUS_FILE):
        return {"bot_running": False, "watching": False, "points": 0, "start_timestamp": 0}
    with open(STATUS_FILE, "r") as f:
        return json.load(f)

def save_status(status):
    with open(STATUS_FILE, "w") as f:
        json.dump(status, f)

def update_status(**kwargs):
    status = load_status()
    status.update(kwargs)
    save_status(status)
