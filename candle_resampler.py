import pandas as pd

def resample_to_weekly(df_daily):
    """
    Convert daily OHLCV DataFrame into weekly candles.
    Weekly open = first open of the week,
    Weekly close = last close of the week,
    High/Low = max/min of the week,
    Volume = sum of weekly volume.
    """
    df = df_daily.copy()
    df.set_index("date", inplace=True)

    df_weekly = df.resample("W").agg({
        "open": "first",
        "high": "max",
        "low": "min",
        "close": "last",
        "volume": "sum"
    }).dropna().reset_index()

    return df_weekly

# Example usage
if __name__ == "__main__":
    from historical_data_fetcher import get_historical_data
    df_daily = get_historical_data("RELIANCE")
    df_weekly = resample_to_weekly(df_daily)
    print(df_weekly.tail())
