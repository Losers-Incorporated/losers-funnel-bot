import csv
from datetime import datetime

def log_action(user_id, action, symbol="", result="", notes=""):
    path = f"users/{user_id}/logs.csv"
    with open(path, "a") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now(), action, symbol, result, notes])
