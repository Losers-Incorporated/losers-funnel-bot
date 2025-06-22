import os
from kiteconnect import KiteConnect
import subprocess

# Load credentials from environment
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
request_token = os.getenv("REQUEST_TOKEN")
github_token = os.getenv("GITHUB_TOKEN")

# ✅ Correct GitHub repo URL format
repo_url = "https://github.com/Losers-Incorporated/losers-funnel-bot.git"
remote_url = repo_url.replace("https://", f"https://{github_token}@")

kite = KiteConnect(api_key=api_key)

try:
    # Generate access token using KiteConnect
    data = kite.generate_session(request_token, api_secret=api_secret)
    access_token = data["access_token"]

    # Save token to file
    with open("access_token.txt", "w") as f:
        f.write(access_token)

    print("✅ Access token saved.")

    # Git configuration and push
    subprocess.run(["git", "config", "--global", "user.email", "cron@bot.com"])
    subprocess.run(["git", "config", "--global", "user.name", "Render Cron Bot"])
    subprocess.run(["git", "init"])
    subprocess.run(["git", "remote", "remove", "origin"], stderr=subprocess.DEVNULL)  # Remove if exists
    subprocess.run(["git", "remote", "add", "origin", remote_url])
    subprocess.run(["git", "add", "access_token.txt"])
    subprocess.run(["git", "commit", "-m", "Update token"])
    subprocess.run(["git", "push", "origin", "main"])

    print("🚀 Token pushed to GitHub.")

except Exception as e:
    print("❌ Failed to generate token:", e)
