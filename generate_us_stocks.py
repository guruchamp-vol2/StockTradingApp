import yfinance as yf
import pandas as pd
import time
import logging
import random
from yahoo_fin import stock_info as si

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pull all tickers (from S&P 500, NASDAQ, Other)
tickers = si.tickers_sp500() + si.tickers_nasdaq() + si.tickers_other()
tickers = list(set(tickers))
random.shuffle(tickers)

# Limit to small batch
tickers = tickers[:11652]
logger.info(f"🎯 Processing {len(tickers)} tickers.")

data = []
failures = []

for i, ticker in enumerate(tickers, 1):
    try:
        # Download recent daily data
        df = yf.download(ticker, period="1d", progress=False)

        if df.empty:
            raise ValueError("No data returned.")

        latest = df.iloc[-1]
        data.append({
            "ticker": ticker,
            "close": latest["Close"],
            "volume": latest["Volume"],
            "open": latest["Open"],
            "high": latest["High"],
            "low": latest["Low"]
        })

        logger.info(f"[{i}/{len(tickers)}] ✅ {ticker} processed.")
        time.sleep(random.uniform(30, 60))

    except Exception as e:
        logger.warning(f"[{i}/{len(tickers)}] ❌ Failed for {ticker}: {e}")
        failures.append(ticker)
        time.sleep(random.uniform(3, 5))

# Save results
df_out = pd.DataFrame(data)
df_out.to_csv("stock_prices.csv", index=False)
logger.info(f"✅ Saved {len(df_out)} records to 'stock_prices.csv'.")

# Save failures
if failures:
    with open("failed_downloads.txt", "w") as f:
        for t in failures:
            f.write(t + "\n")
    logger.warning(f"⚠️ {len(failures)} tickers failed. Saved to 'failed_downloads.txt'.")
