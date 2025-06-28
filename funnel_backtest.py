import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator

# --- Utility Functions ---
def calculate_slope(close_prices):
    """Calculate linear slope in degrees over last N weeks"""
    y = np.log(close_prices)
    x = np.arange(len(y))
    if len(x) < 2:
        return 0
    slope, _ = np.polyfit(x, y, 1)
    return round(np.degrees(np.arctan(slope)), 2)

def calculate_rsi(close, period=14):
    """RSI calculation using ta-lib logic"""
    return RSIIndicator(close).rsi()

def is_volume_boosted(volume_series):
    """Volume check: last week's vol > 1.5x average of past 8 weeks"""
    if len(volume_series) < 9:
        return False
    return volume_series[-1] > 1.5 * volume_series[-9:-1].mean()

# --- Main Funnel Analyzer ---
def analyze_funnel(df):
    df = df.copy()
    df["slope_deg"] = df["close"].rolling(window=6).apply(calculate_slope, raw=False)
    df["rsi"] = calculate_rsi(df["close"])
    df["volume_boost"] = df["volume"].rolling(window=9).apply(is_volume_boosted, raw=False)

    latest = df.iloc[-1]
    signal = {}

    # --- Conditions ---
    signal["slope"] = latest["slope_deg"]
    signal["rsi"] = latest["rsi"]
    signal["volume_boost"] = bool(latest["volume_boost"])
    signal["funnel_pattern"] = False

    if latest["slope_deg"] > 5 and latest["rsi"] > 50 and signal["volume_boost"]:
        # Entry logic — breakout with confirmation
        signal["entry"] = latest["close"]
        signal["stop"] = df["low"].iloc[-3:-1].min()  # recent support
        signal["target"] = round(signal["entry"] + 2.5 * (signal["entry"] - signal["stop"]), 2)
        signal["risk"] = "🟢 Confirmed Funnel Breakout"
        signal["funnel_pattern"] = True
    else:
        signal["entry"] = None
        signal["stop"] = None
        signal["target"] = None
        signal["risk"] = "🔴 No Confirmed Signal"

    return signal
