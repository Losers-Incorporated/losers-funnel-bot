import pandas as pd
from instrument_loader import load_instruments, load_sector_mapping
from funnel_backtest import analyze_stock
from output_formatter import format_output_table


def batch_backtest_all():
    # Load instruments and sector mapping
    all_instruments = load_instruments()
    sector_map = load_sector_mapping()

    results = []

    for sector, symbols in sector_map.items():
        for symbol in symbols:
            try:
                result = analyze_stock(symbol)
                if result:
                    result["Sector"] = sector
                    results.append(result)
            except Exception as e:
                print(f"❌ Error processing {symbol}: {e}")

    # Convert to DataFrame and format
    if results:
        df = pd.DataFrame(results)
        print(format_output_table(df))
    else:
        print("⚠️ No valid results produced.")


if __name__ == "__main__":
    batch_backtest_all()
