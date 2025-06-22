import os
import subprocess
import tempfile
import shutil
from kiteconnect import KiteConnect

# Load credentials
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
request_token = os.getenv("REQUEST_TOKEN")
github_token = os.getenv("GITHUB_TOKEN")

# GitHub repo URL
repo_url = "https://github.com/Losers-Incorporated/losers-funnel-bot.git"
remote_url = repo_url.replace("https://", f"https://{github_token}@")

# Create a temporary working directory
with tempfile.TemporaryDirectory() as tmpdir:
    os.chdir(tmpdir)
    subprocess.run(["git", "clone", remote_url, "."], check=True)

    # Generate token using KiteConnect
    kite = KiteConnect(api_key=api_key)
    try:
        data = kite.generate_session(request_token, api_secret=api_secret)
        access_token = data["access_token"]

        with open("access_token.txt", "w") as f:
            f.write(access_token)
        print("✅ Access token saved.")

        subprocess.run(["git", "config", "user.email", "cron@bot.com"], check=True)
        subprocess.run(["git", "config", "user.name", "Render Cron Bot"], check=True)
        subprocess.run(["git", "add", "access_token.txt"], check=True)
        subprocess.run(["git", "commit", "-m", "Update token"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("🚀 Token pushed to GitHub.")

    except Exception as e:
        print("❌ Failed to generate token:", e)
