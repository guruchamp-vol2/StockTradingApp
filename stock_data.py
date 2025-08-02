# stock_data.py
import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("FINNHUB_API_KEY")
BASE = "https://finnhub.io/api/v1"

def get_profile(symbol):
    url = f"{BASE}/stock/profile2?symbol={symbol}&token={API_KEY}"
    res = requests.get(url)
    return res.json()

def get_candles(symbol, resolution="D", days=365):
    now = int(time.time())
    past = now - days * 86400
    url = f"{BASE}/stock/candle?symbol={symbol}&resolution={resolution}&from={past}&to={now}&token={API_KEY}"
    res = requests.get(url)
    return res.json()
