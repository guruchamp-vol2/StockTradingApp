import yfinance as yf
import pandas as pd
import numpy as np
import requests
from ta.momentum import RSIIndicator
from ta.trend import MACD
from textblob import TextBlob
from newsapi import NewsApiClient
from dotenv import load_dotenv
import os
import time

# Load API keys
load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

newsapi = NewsApiClient(api_key=NEWS_API_KEY)


def fetch_price_data(ticker, period="6mo", interval="1d"):
    """Fetch historical price data using yfinance."""
    try:
        df = yf.download(ticker, period=period, interval=interval, progress=False)
        if df.empty:
            return None
        return df
    except Exception as e:
        print(f"[ERROR] Fetching price data for {ticker}: {e}")
        return None


def compute_technical_indicators(df):
    """Compute RSI, MACD and SMA indicators."""
    indicators = {}
    try:
        close = df["Close"]

        # RSI
        rsi = RSIIndicator(close).rsi().iloc[-1]
        indicators["rsi"] = round(rsi, 2)

        # MACD
        macd_line = MACD(close).macd()
        signal_line = MACD(close).macd_signal()
        indicators["macd_trend"] = "Bullish" if macd_line.iloc[-1] > signal_line.iloc[-1] else "Bearish"

        # SMA
        indicators["sma_50"] = round(close.rolling(50).mean().iloc[-1], 2)
        indicators["sma_200"] = round(close.rolling(200).mean().iloc[-1], 2)

        return indicators
    except Exception as e:
        print(f"[ERROR] Computing indicators: {e}")
        return {}


def analyze_news_sentiment(ticker):
    """Fetch recent news and analyze sentiment."""
    try:
        query = f"{ticker} stock"
        articles = newsapi.get_everything(q=query, language="en", sort_by="publishedAt", page_size=5)
        scores = []

        for article in articles.get("articles", []):
            title = article.get("title", "")
            if title:
                score = TextBlob(title).sentiment.polarity
                scores.append(score)

        if scores:
            sentiment = round(np.mean(scores), 3)
            return sentiment
        return 0.0
    except Exception as e:
        print(f"[ERROR] Analyzing sentiment for {ticker}: {e}")
        return 0.0


def score_stock(ticker):
    """Score a single stock based on indicators and sentiment."""
    df = fetch_price_data(ticker)
    if df is None or len(df) < 60:
        return None

    tech = compute_technical_indicators(df)
    sentiment = analyze_news_sentiment(ticker)

    if not tech:
        return None

    # Score logic (0–1 scale)
    trend_score = 1 if tech["sma_50"] > tech["sma_200"] else 0
    rsi_score = 1 if 40 < tech["rsi"] < 70 else 0
    sentiment_score = 1 if sentiment > 0.1 else 0

    final_score = round((0.4 * trend_score) + (0.3 * rsi_score) + (0.3 * sentiment_score), 2)

    return {
        "ticker": ticker,
        "score": final_score,
        "rsi": tech["rsi"],
        "macd_trend": tech["macd_trend"],
        "sentiment": sentiment,
        "sma_50": tech["sma_50"],
        "sma_200": tech["sma_200"],
    }


def run_screener(tickers, delay=12):
    """Run the screener over a list of tickers with API rate safety."""
    results = []
    for i, ticker in enumerate(tickers):
        print(f"🧪 Screening {ticker} ({i+1}/{len(tickers)})...")
        data = score_stock(ticker)
        if data:
            results.append(data)
        time.sleep(delay)  # API safe pause
    return sorted(results, key=lambda x: x["score"], reverse=True)


if __name__ == "__main__":
    # Example tickers (replace with full list later)
    sample = ["AAPL", "MSFT", "TSLA", "NVDA", "AMZN"]
    results = run_screener(sample)

    print("\n🏆 Top Stocks:")
    for r in results:
        print(f"{r['ticker']} | Score: {r['score']} | RSI: {r['rsi']} | Sentiment: {r['sentiment']} | Trend: {r['macd_trend']}")
