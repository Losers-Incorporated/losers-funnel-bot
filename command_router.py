def route_command(user_input):
    user_input = user_input.lower().strip()

    if user_input.startswith("analyze "):
        symbol = user_input.replace("analyze ", "").strip().upper()
        return ("analyze_stock", symbol)

    elif user_input.startswith("scan ") and "sector" in user_input:
        sector = user_input.replace("scan ", "").replace("sector", "").strip().title()
        return ("analyze_sector", sector)

    elif user_input.startswith("backtest "):
        symbol = user_input.replace("backtest ", "").strip().upper()
        return ("backtest_stock", symbol)

    else:
        return ("unknown", user_input)

# Example usage
if __name__ == "__main__":
    cmds = [
        "Analyze Reliance",
        "Scan Power Sector",
        "Backtest Suzlon",
        "Unknown command test"
    ]
    
    for cmd in cmds:
        print(f"Input: {cmd} → Routed: {route_command(cmd)}")
