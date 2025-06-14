import os
import json

def create_user_profile(user_id, username):
    path = f"users/{user_id}/"
    if not os.path.exists(path):
        os.makedirs(path)
        open(f"{path}logs.csv", "w").write("timestamp,action,symbol,result,notes\n")
        with open(f"{path}watchlist.json", "w") as f:
            json.dump([], f)
        with open(f"{path}config.json", "w") as f:
            json.dump({"username": username}, f)
        print(f"[✓] Created profile for {username} ({user_id})")
