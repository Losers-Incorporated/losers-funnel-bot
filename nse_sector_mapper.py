# ✅ Updated: nse_sector_mapper.py (Auto-fetch NSE stock-sector mapping)
# Saves output as sector_mapping_nse.csv

import requests
import pandas as pd
import time

BASE_URL = "https://www.nseindia.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Referer": "https://www.nseindia.com/"
}

SECTORS = [
    "AUTO", "BANK", "FINANCE", "IT", "FMCG", "OILGAS",
    "METAL", "PHARMA", "HEALTHCARE", "TEXTILES", "ENERGY",
    "REALTY", "TELECOM", "CHEMICAL", "CAPITALGOODS"
]

OUTPUT_FILE = "sector_mapping_nse.csv"

def fetch_sector_stocks(sector):
    try:
        url = f"https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20{sector.upper()}"
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        data = response.json()
        return [
            {"tradingsymbol": stock["symbol"], "sector": sector.capitalize()}
            for stock in data.get("data", [])
        ]
    except Exception as e:
        print(f"❌ Failed to fetch {sector}: {e}")
        return []

def main():
    all_entries = []
    for sector in SECTORS:
        entries = fetch_sector_stocks(sector)
        all_entries.extend(entries)
        time.sleep(1)  # avoid rate-limiting

    df = pd.DataFrame(all_entries).drop_duplicates()
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ {OUTPUT_FILE} written with {len(df)} entries.")

if __name__ == "__main__":
    main()
