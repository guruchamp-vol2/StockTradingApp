import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("FINNHUB_API_KEY")

def fetch_us_tickers():
    url = f"https://finnhub.io/api/v1/stock/symbol?exchange=US&token={API_KEY}"
    response = requests.get(url).json()
    df = pd.DataFrame(response)
    df = df[['symbol', 'displaySymbol', 'description', 'type']]
    df.to_csv("active_us_tickers.csv", index=False)
    print(f"✅ {len(df)} tickers saved to active_us_tickers.csv")

if __name__ == "__main__":
    fetch_us_tickers()

