import pandas as pd

def load_csv_safely(path):
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        print(f"[!] {path} not found.")
        return pd.DataFrame(columns=["tradingsymbol", "sector"])

# Load all 3 sources
nse_df = load_csv_safely("sector_mapping_nse.csv")
bse_df = load_csv_safely("sector_mapping_bse.csv")
manual_df = load_csv_safely("sector_manual_override.csv")

# Combine and deduplicate
combined_df = pd.concat([nse_df, bse_df], ignore_index=True)
combined_df.drop_duplicates(subset=["tradingsymbol"], keep="first", inplace=True)

# Manual overrides → overwrite any entries in combined_df
manual_df.set_index("tradingsymbol", inplace=True)
combined_df.set_index("tradingsymbol", inplace=True)
combined_df.update(manual_df)
combined_df.reset_index(inplace=True)

# Save merged file
combined_df.to_csv("sector_mapping.csv", index=False)
print(f"[✓] sector_mapping.csv generated with {len(combined_df)} entries.")
