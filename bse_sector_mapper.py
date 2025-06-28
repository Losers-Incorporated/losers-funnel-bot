# ✅ Final: bse_sector_mapper.py (Simulated BSE stock-sector mapping)
import csv

# ⚠️ Note: BSE does not offer an open sector-wise API like NSE.
# This script uses a manually curated list of key BSE stocks with sectors.

BSE_SIMULATED_MAPPING = {
    '500325': ('RELIANCE', 'Energy'),
    '532540': ('TCS', 'IT'),
    '500209': ('INFY', 'IT'),
    '532174': ('ICICIBANK', 'Bank'),
    '500180': ('HDFCBANK', 'Bank'),
    '500112': ('SBIN', 'Bank'),
    '500696': ('HINDUNILVR', 'FMCG'),
    '500124': ('DRREDDY', 'Pharma'),
    '543320': ('ZOMATO', 'Consumer Tech'),
    '500002': ('ABB', 'Capital Goods'),
    '500010': ('HDFC', 'Finance'),
    '500247': ('KOTAKBANK', 'Bank'),
    # 🔧 Add more as needed
}

OUTPUT_CSV = "sector_mapping_bse.csv"

def write_bse_sector_mapping():
    with open(OUTPUT_CSV, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['tradingsymbol', 'sector'])
        for _, (symbol, sector) in BSE_SIMULATED_MAPPING.items():
            writer.writerow([symbol, sector])
    print(f"✅ {OUTPUT_CSV} written with {len(BSE_SIMULATED_MAPPING)} entries.")

if __name__ == '__main__':
    write_bse_sector_mapping()
