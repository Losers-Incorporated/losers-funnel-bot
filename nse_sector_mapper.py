import pandas as pd

# 1. Define NSE sector indices to fetch
SECTOR_INDICES = {
    "Auto": "AUTO",
    "Bank": "BANK",
    "FMCG": "FAST_AUG",
    "HealthCare": "HEALTHCARE",
    "IT": "IT",
    "Metal": "METAL",
    "OilGas": "OIL_GAS",
    "Pharma": "PHARMA",
    "Realty": "REALTY",
    "Energy": "ENERGY",
}

# 2. Base URL for NSE index constituent CSVs
BASE_URL = "https://www.nseindia.com/content/indices/ind_{0}list.csv"

def fetch_sector_symbols(index_key):
    url = BASE_URL.format(index_key.lower())
    df = pd.read_csv(url)
    return df["Symbol"].astype(str).str.upper().tolist()

def build_sector_mapping():
    mapping = []
    for sector, idx in SECTOR_INDICES.items():
        try:
            symbols = fetch_sector_symbols(idx)
            for sym in symbols:
                mapping.append({"tradingsymbol": sym, "sector": sector})
            print(f"✅ Loaded {len(symbols)} symbols for sector: {sector}")
        except Exception as e:
            print(f"❌ Failed to fetch {sector}: {e}")

    # Combine and dedupe
    df = pd.DataFrame(mapping).drop_duplicates("tradingsymbol")
    print(f"🧮 Total symbols mapped: {len(df)}")
    
    # 3. Optionally tag unclassified symbols (those not in this mapping)
    # Uncomment to include:
    # from instrument_loader import load_all_instruments
    # all_syms = set(load_all_instruments()["tradingsymbol"])
    # unclassified = all_syms - set(df["tradingsymbol"])
    # df = pd.concat([df, pd.DataFrame([{"tradingsymbol": sym, "sector": "Unclassified"} for sym in unclassified])])

    # Save mapping
    df.to_csv("sector_mapping.csv", index=False)
    print("✅ sector_mapping.csv written successfully.")

if __name__ == "__main__":
    build_sector_mapping()
