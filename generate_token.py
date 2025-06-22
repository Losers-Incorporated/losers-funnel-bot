import os
from kiteconnect import KiteConnect
import subprocess

# Load credentials from environment
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
request_token = os.getenv("REQUEST_TOKEN")
github_token = os.getenv("GITHUB_TOKEN")
repo_url = "github.com/Losers-Incorporated/losers-funnel-bot.git"

kite = KiteConnect(api_key=api_key)

try:
    data = kite.generate_session(request_token, api_secret=api_secret)
    access_token = data["access_token"]

    # Save token to file
    with open("access_token.txt", "w") as f:
        f.write(access_token)

    print("✅ Access token saved.")

    # Configure and push via GitHub token
    subprocess.run(["git", "config", "--global", "user.email", "cron@bot.com"])
    subprocess.run(["git", "config", "--global", "user.name", "Render Cron Bot"])
    subprocess.run(["git", "add", "access_token.txt"])
    subprocess.run(["git", "commit", "-m", "Update token"])
    subprocess.run([
        "git", "push",
        f"https://{github_token}@{repo_url}",
        "main"
    ])

    print("🚀 Token pushed to GitHub.")

except Exception as e:
    print("❌ Failed to generate token:", e)
