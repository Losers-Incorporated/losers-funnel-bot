import os
from kiteconnect import KiteConnect
import subprocess

# Load credentials from environment
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
request_token = os.getenv("REQUEST_TOKEN")

kite = KiteConnect(api_key=api_key)

# Generate access token
try:
    data = kite.generate_session(request_token, api_secret=api_secret)
    access_token = data["access_token"]

    # Save token to file
    with open("access_token.txt", "w") as f:
        f.write(access_token)

    print("✅ Access token saved.")

    # Git commit & push
    subprocess.run(["git", "config", "--global", "user.email", "cron@bot.com"])
    subprocess.run(["git", "config", "--global", "user.name", "Render Cron Bot"])
    subprocess.run(["git", "add", "access_token.txt"])
    subprocess.run(["git", "commit", "-m", "Update token"])
    subprocess.run(["git", "push", "origin", "main"])

    print("🚀 Token pushed to GitHub.")

except Exception as e:
    print("❌ Failed to generate token:", e)
