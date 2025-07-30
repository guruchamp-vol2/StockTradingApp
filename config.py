import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration settings for the stock analysis app"""
    
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    NEWS_API_KEY = os.getenv('NEWS_API_KEY', '')
    ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY', '')
    
    # Application Settings
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Stock Analysis Settings
    MIN_MARKET_CAP = 1000000000  # $1B minimum market cap
    MIN_VOLUME = 1000000  # 1M minimum volume
    MAX_PE_RATIO = 50  # Maximum P/E ratio for value stocks
    MIN_ROE = 0.10  # Minimum 10% ROE
    
    # Technical Analysis Settings
    RSI_OVERSOLD = 30
    RSI_OVERBOUGHT = 70
    MA_SHORT = 20
    MA_LONG = 50
    
    # News Analysis Settings
    NEWS_LOOKBACK_DAYS = 7
    SENTIMENT_THRESHOLD = 0.1
    
    # Scoring Weights
    FUNDAMENTAL_WEIGHT = 0.4
    TECHNICAL_WEIGHT = 0.3
    SENTIMENT_WEIGHT = 0.2
    GROWTH_WEIGHT = 0.1 