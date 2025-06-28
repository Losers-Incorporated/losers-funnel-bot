import pandas as pd
from pathlib import Path

# Load data from all 3 sources
nse_file = Path("sector_mapping_nse.csv")
bse_file = Path("sector_mapping_bse.csv")
override_file = Path("sector_manual_override.csv")

dfs = []

# Load NSE if it exists
if nse_file.exists():
    dfs.append(pd.read_csv(nse_file))

# Load BSE if it exists
if bse_file.exists():
    dfs.append(pd.read_csv(bse_file))

# Combine NSE + BSE
combined = pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame(columns=["tradingsymbol", "sector"])

# Drop duplicates by symbol, keep first
combined = combined.drop_duplicates(subset="tradingsymbol", keep="first")

# Load manual overrides
if override_file.exists():
    manual_df = pd.read_csv(override_file)
    
    # Remove entries that exist in manual override
    combined = combined[~combined["tradingsymbol"].isin(manual_df["tradingsymbol"])]

    # Append manual rows at the end
    combined = pd.concat([combined, manual_df], ignore_index=True)

# Sort and save final master file
combined = combined.sort_values(by="tradingsymbol").reset_index(drop=True)
combined.to_csv("sector_mapping.csv", index=False)

print(f"✅ sector_mapping.csv generated with {len(combined)} entries.")
