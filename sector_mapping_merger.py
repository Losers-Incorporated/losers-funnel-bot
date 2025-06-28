import pandas as pd
from pathlib import Path

# File paths
nse_file = Path("sector_mapping_nse.csv")
bse_file = Path("sector_mapping_bse.csv")
override_file = Path("sector_manual_override.csv")
output_file = Path("sector_mapping.csv")

dfs = []

# Load NSE mappings
if nse_file.exists():
    nse_df = pd.read_csv(nse_file)
    print(f"✅ Loaded NSE sector mapping: {len(nse_df)} entries")
    dfs.append(nse_df)
else:
    print("⚠️ NSE file missing")

# Load BSE mappings
if bse_file.exists():
    bse_df = pd.read_csv(bse_file)
    print(f"✅ Loaded BSE sector mapping: {len(bse_df)} entries")
    dfs.append(bse_df)
else:
    print("⚠️ BSE file missing")

# Combine NSE + BSE
combined_df = pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame(columns=["tradingsymbol", "sector"])
combined_df = combined_df.drop_duplicates(subset="tradingsymbol", keep="first")

# Load manual override and apply
if override_file.exists():
    override_df = pd.read_csv(override_file)
    print(f"✅ Loaded manual overrides: {len(override_df)} entries")

    # Remove overridden rows from combined
    combined_df = combined_df[~combined_df["tradingsymbol"].isin(override_df["tradingsymbol"])]

    # Append manual overrides
    combined_df = pd.concat([combined_df, override_df], ignore_index=True)
else:
    print("⚠️ Manual override file missing")

# Final sort and save
combined_df = combined_df.sort_values(by="tradingsymbol").reset_index(drop=True)
combined_df.to_csv(output_file, index=False)

print(f"✅ {output_file.name} written with {len(combined_df)} final entries.")
