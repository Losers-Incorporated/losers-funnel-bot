import csv
import os
from nsetools import Nse
from time import sleep

# NOTE: This BSE simulation assumes limited symbol-to-sector mapping due to lack of BSE's structured API like NSE
# For full-scale integration, tie-in with 3rd-party or licensed BSE datasets

BSE_SIMULATED_MAPPING = {
    '500325': ('RELIANCE', 'Energy'),
    '532540': ('TCS', 'IT'),
    '500209': ('INFY', 'IT'),
    '532174': ('ICICIBANK', 'Bank'),
    '500180': ('HDFCBANK', 'Bank'),
    '500112': ('SBIN', 'Bank'),
    '500696': ('HINDUNILVR', 'FMCG'),
    '500124': ('DRREDDY', 'Pharma'),
    '532321': ('ZOMATO', 'Consumer Tech'),
    # Extend as needed
}

OUTPUT_CSV = "sector_mapping_bse.csv"

def write_bse_sector_mapping():
    with open(OUTPUT_CSV, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['tradingsymbol', 'sector'])

        for bse_code, (symbol, sector) in BSE_SIMULATED_MAPPING.items():
            writer.writerow([symbol, sector])

    print(f"✅ sector_mapping_bse.csv written with {len(BSE_SIMULATED_MAPPING)} entries.")


if __name__ == '__main__':
    write_bse_sector_mapping()
