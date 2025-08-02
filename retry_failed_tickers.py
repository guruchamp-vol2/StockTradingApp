# retry_failed_tickers.py
import yfinance as yf
import pandas as pd
import time
import logging
import random

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load failed tickers from file
with open("failed_tickers.txt") as f:
    tickers = [line.strip() for line in f if line.strip()]

logger.info(f"Retrying {len(tickers)} failed tickers...")

data = []
failures = []

def get_market_cap_category(market_cap):
    if market_cap is None:
        return "Unknown"
    elif market_cap >= 10_000_000_000:
        return "Large Cap"
    elif market_cap >= 2_000_000_000:
        return "Mid Cap"
    elif market_cap >= 300_000_000:
        return "Small Cap"
    else:
        return "Micro Cap"

for i, ticker in enumerate(tickers, 1):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        name = info.get("shortName", "N/A")
        exchange = info.get("exchange", "N/A")
        sector = info.get("sector", "N/A")
        market_cap = info.get("marketCap", None)
        cap_category = get_market_cap_category(market_cap)

        data.append({
            "ticker": ticker,
            "exchange": exchange,
            "company_name": name,
            "sector": sector,
            "market_cap_category": cap_category
        })

        logger.info(f"[{i}/{len(tickers)}] {ticker} ✅")

        time.sleep(random.uniform(6.0, 10.0))

    except Exception as e:
        logger.warning(f"Retry failed for {ticker}: {e}")
        failures.append(ticker)
        time.sleep(random.uniform(1.5, 3.0))

# Save new results to a separate file
df = pd.DataFrame(data)
df.to_csv("retried_successful.csv", index=False)
logger.info(f"Saved {len(df)} retried stocks to 'retried_successful.csv'.")

# Save remaining failures
if failures:
    with open("still_failed_tickers.txt", "w") as f:
        for t in failures:
            f.write(t + "\n")
    logger.warning(f"⚠️ {len(failures)} tickers failed again. Saved to 'still_failed_tickers.txt'.")
