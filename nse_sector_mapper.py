import requests
import pandas as pd
import time

SECTORS = [
    "FMCG", "IT", "Energy", "Pharma", "Auto",
    "Bank", "Metal", "Realty", "OilGas", "FinancialServices",
    "Healthcare"
]

BASE_URL = "https://www1.nseindia.com/live_market/dynaContent/live_watch/stock_watch/{}StockWatch.json"
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www1.nseindia.com/live_market/dynaContent/live_watch/stock_watch/niftyStockWatch.htm"
}

def fetch_sector_stocks(sector):
    url = BASE_URL.format(sector)
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        data = response.json()
        return [
            {"tradingsymbol": entry["symbol"].strip(), "sector": sector}
            for entry in data.get("data", [])
        ]
    except Exception as e:
        print(f"Failed to fetch {sector}: {e}")
        return []

def build_sector_mapping():
    all_data = []
    for sector in SECTORS:
        stocks = fetch_sector_stocks(sector)
        print(f"Fetched {len(stocks)} from {sector}")
        all_data.extend(stocks)
        time.sleep(1)  # Be polite to the server

    df = pd.DataFrame(all_data)
    df.to_csv("sector_mapping.csv", index=False)
    print(f"✅ sector_mapping.csv written with {len(df)} entries.")

if __name__ == "__main__":
    build_sector_mapping()
