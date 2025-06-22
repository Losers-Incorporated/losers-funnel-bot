import os
from kiteconnect import KiteConnect

kite = KiteConnect(api_key=os.getenv("API_KEY"))
request_token = os.getenv("REQUEST_TOKEN")
api_secret = os.getenv("API_SECRET")

data = kite.generate_session(request_token, api_secret=api_secret)
kite.set_access_token(data["access_token"])

print("✅ Access token generated successfully.")
print("Access Token:", data["access_token"])

# Optional: save to file
with open("access_token.txt", "w") as f:
    f.write(data["access_token"])
