import os
import pandas as pd
from kiteconnect import KiteConnect
from datetime import datetime, timedelta

# Initialize Kite with environment variable
kite = KiteConnect(api_key=os.getenv("KITE_API_KEY"))

# Load access token from file
with open("access_token.txt", "r") as f:
    kite.set_access_token(f.read().strip())

def get_instrument_token(trading_symbol):
    """Get instrument token for NSE stock symbol"""
    instruments = pd.DataFrame(kite.instruments("NSE"))
    match = instruments[instruments["tradingsymbol"] == trading_symbol.upper()]
    if not match.empty:
        return int(match.iloc[0]["instrument_token"])
    raise ValueError(f"Instrument not found for: {trading_symbol}")

def get_historical_data(symbol, days=395):
    """Fetch 395 days of daily OHLCV data"""
    instrument_token = get_instrument_token(symbol)
    to_date = datetime.today()
    from_date = to_date - timedelta(days=days)

    data = kite.historical_data(
        instrument_token,
        from_date,
        to_date,
        interval="day",
        continuous=False,
        oi=False
    )
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])
    return df

# Batch fetch for multiple stocks
if __name__ == "__main__":
    TICKERS = ["RELIANCE", "INFY", "HDFCBANK", "LT", "SBIN"]  # Modify as needed

    for symbol in TICKERS:
        try:
            df = get_historical_data(symbol)
            df.to_csv(f"{symbol}_OHLC.csv", index=False)
            print(f"✅ Saved {symbol}_OHLC.csv")
        except Exception as e:
            print(f"❌ Failed for {symbol}: {e}")
