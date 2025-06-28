import os
import csv
import json
from datetime import datetime

# 🔹 1. Per-User CSV Logger
def log_action(user_id, action, symbol="", result="", notes=""):
    os.makedirs(f"users/{user_id}", exist_ok=True)
    path = f"users/{user_id}/logs.csv"
    with open(path, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().isoformat(), action, symbol, result, notes])


# 🔹 2. Engine-Level Signal Logger (JSON, daily)
def write_log(command: str, result: dict, outcome: str = "pending"):
    os.makedirs("logs", exist_ok=True)
    log_path = f"logs/{datetime.now().date()}.json"

    # Load existing logs if present
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            logs = json.load(f)
    else:
        logs = []

    logs.append({
        "timestamp": datetime.now().isoformat(),
        "command": command,
        "result": result,
        "outcome": outcome
    })

    with open(log_path, "w") as f:
        json.dump(logs, f, indent=2)

