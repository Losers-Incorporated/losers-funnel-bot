import pandas as pd

def format_funnel_output(results):
    """
    Takes a list of dicts with stock signal results and returns a formatted Markdown table.
    """
    if not results:
        return "⚠️ No valid funnel entries found."

    df = pd.DataFrame(results)

    # Ensure all expected columns exist
    expected_columns = [
        "Stock", "Week", "Signal", "Funnel Type", "Entry Price",
        "Stop Loss", "Target Zone", "Volume", "RSI", "Remarks",
        "ATR Buffer", "Slope Score", "Volume Spike", "Institutional Bias", "Setup Age"
    ]
    for col in expected_columns:
        if col not in df.columns:
            df[col] = "—"

    # Reorder and rename for readability
    df = df[expected_columns]
    df.columns = [
        "📈 Stock", "📅 Week", "🔔 Signal", "🔹 Type", "🎯 Entry",
        "🛑 Stop", "📍 Target", "📊 Volume", "📈 RSI", "📝 Remarks",
        "ATR 📏", "Slope 📐", "Vol Spike 🔍", "Inst Bias 🏦", "⏳ Age (wks)"
    ]

    return df.to_markdown(index=False)

# Example usage for test
if __name__ == "__main__":
    mock_results = [
        {
            "Stock": "RELIANCE", "Week": "2025-06-28", "Signal": "✅ Breakout", "Funnel Type": "Pullback",
            "Entry Price": 2700, "Stop Loss": 2635, "Target Zone": 2825, "Volume": "+68%", "RSI": 62,
            "Remarks": "Strong close above resistance zone",
            "ATR Buffer": "22 pts", "Slope Score": "8.1", "Volume Spike": "Yes",
            "Institutional Bias": "Yes", "Setup Age": "3"
        }
    ]
    print(format_funnel_output(mock_results))
