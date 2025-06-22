import os
import subprocess
import tempfile
from kiteconnect import KiteConnect

# Load credentials from environment
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
request_token = os.getenv("REQUEST_TOKEN")
github_token = os.getenv("GITHUB_TOKEN")

# GitHub repo details
repo_url = "https://github.com/Losers-Incorporated/losers-funnel-bot.git"
remote_url = repo_url.replace("https://", f"https://{github_token}@")

# Step 1: Generate access token early
kite = KiteConnect(api_key=api_key)
try:
    data = kite.generate_session(request_token, api_secret=api_secret)
    access_token = data["access_token"]
    print("✅ Token generated successfully.")

except Exception as e:
    print("❌ Failed to generate token:", e)
    exit(1)

# Step 2: Clone repo and push token
with tempfile.TemporaryDirectory() as tmpdir:
    print(f"📂 Using temp dir: {tmpdir}")
    os.chdir(tmpdir)
    subprocess.run(["git", "clone", remote_url, "."], check=True)
    print("✅ Repo cloned. Files:", os.listdir())

    # Write token file
    with open("access_token.txt", "w") as f:
        f.write(access_token)
    print("💾 Token written to access_token.txt")

    # Git config and commit
    subprocess.run(["git", "config", "user.email", "cron@bot.com"], check=True)
    subprocess.run(["git", "config", "user.name", "Render Cron Bot"], check=True)
    subprocess.run(["git", "add", "access_token.txt"], check=True)
    subprocess.run(["git", "commit", "-m", "Update token"], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)

    print("🚀 Token committed and pushed to GitHub.")
