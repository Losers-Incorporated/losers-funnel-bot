import pandas as pd
import os

# File paths
auto_file = "sector_mapping_auto.csv"
manual_file = "sector_manual_override.csv"
output_file = "sector_mapping.csv"

def merge_sector_mappings():
    # Load auto-mapped file
    if os.path.exists(auto_file):
        auto_df = pd.read_csv(auto_file)
    else:
        auto_df = pd.DataFrame(columns=["tradingsymbol", "sector"])

    # Load manual override file
    if os.path.exists(manual_file):
        manual_df = pd.read_csv(manual_file)
    else:
        manual_df = pd.DataFrame(columns=["tradingsymbol", "sector"])

    # Merge with manual taking precedence
    combined_df = pd.concat([auto_df, manual_df])
    final_df = combined_df.drop_duplicates(subset="tradingsymbol", keep="last")
    final_df = final_df.sort_values(by="tradingsymbol")

    # Save output
    final_df.to_csv(output_file, index=False)
    print(f"✅ sector_mapping.csv generated with {len(final_df)} entries.")

if __name__ == "__main__":
    merge_sector_mappings()
