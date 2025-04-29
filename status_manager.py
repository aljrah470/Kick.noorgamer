import json
import os

STATUS_FILE = "bot_status.json"

# حالة افتراضية في حال عدم وجود ملف سابق
default_status = {
    "bot_running": False,
    "watching": False,
    "points": 0,
    "start_timestamp": 0
}

def load_status():
    if not os.path.exists(STATUS_FILE):
        return default_status.copy()
    try:
        with open(STATUS_FILE, "r") as file:
            return json.load(file)
    except Exception:
        return default_status.copy()

def save_status(bot_running, watching, points, start_timestamp):
    status = {
        "bot_running": bot_running,
        "watching": watching,
        "points": points,
        "start_timestamp": start_timestamp
    }
    with open(STATUS_FILE, "w") as file:
        json.dump(status, file)
