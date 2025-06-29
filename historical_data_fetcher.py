import os
import pandas as pd
from kiteconnect import KiteConnect
from datetime import datetime, timedelta

# === Load API key & token ===
kite = KiteConnect(api_key=os.getenv("KITE_API_KEY"))

with open("access_token.txt", "r") as f:
    kite.set_access_token(f.read().strip())

# === List of NSE stocks to fetch ===
STOCK_LIST = ["RELIANCE", "INFY", "TCS", "HDFCBANK", "ICICIBANK"]

# === Create data folder if it doesn't exist ===
os.makedirs("data", exist_ok=True)

# === Token fetcher ===
def get_instrument_token(symbol):
    instruments = pd.DataFrame(kite.instruments("NSE"))
    row = instruments[instruments["tradingsymbol"] == symbol.upper()]
    if not row.empty:
        return int(row.iloc[0]["instrument_token"])
    raise ValueError(f"Instrument token not found for {symbol}")

# === Historical fetcher ===
def get_historical_data(symbol, days=395):
    token = get_instrument_token(symbol)
    to_date = datetime.today()
    from_date = to_date - timedelta(days=days)

    data = kite.historical_data(
        token, from_date, to_date, interval="day", continuous=False, oi=False
    )
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])
    return df

# === Run for all stocks ===
if __name__ == "__main__":
    for stock in STOCK_LIST:
        try:
            df = get_historical_data(stock)
            filename = f"data/{stock}_{datetime.today().strftime('%Y%m%d')}.csv"
            df.to_csv(filename, index=False)
            print(f"✅ Saved: {filename}")
        except Exception as e:
            print(f"❌ Error for {stock}: {e}")
