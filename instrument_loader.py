import pandas as pd
from kiteconnect import KiteConnect
import os

kite = KiteConnect(api_key=os.getenv("API_KEY"))
with open("access_token.txt") as f:
    kite.set_access_token(f.read().strip())

def load_all_instruments():
    nse = pd.DataFrame(kite.instruments("NSE"))
    bse = pd.DataFrame(kite.instruments("BSE"))
    df = pd.concat([nse, bse], ignore_index=True)
    return df[["exchange", "segment", "tradingsymbol", "instrument_token"]]
