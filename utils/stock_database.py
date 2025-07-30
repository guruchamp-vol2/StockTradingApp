import pandas as pd
import requests
import yfinance as yf
from typing import List, Dict, Optional
import logging
from datetime import datetime
import time
from pathlib import Path

class StockDatabase:
    """Comprehensive database of US stocks"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.stocks_cache = None
        self.last_update = None
        self.cache_duration = 24 * 60 * 60  # 24 hours in seconds
    
    def get_all_us_stocks(self) -> List[Dict]:
        """Get comprehensive list of US stocks"""
        try:
            # Try to get from cache first
            if self._is_cache_valid():
                return self.stocks_cache
            
            # Get stocks from multiple sources
            stocks = []
            
            # Source 1: NASDAQ stocks
            nasdaq_stocks = self._get_nasdaq_stocks()
            stocks.extend(nasdaq_stocks)
            
            # Source 2: NYSE stocks
            nyse_stocks = self._get_nyse_stocks()
            stocks.extend(nyse_stocks)
            
            # Source 3: Popular stocks (backup)
            popular_stocks = self._get_popular_stocks()
            stocks.extend(popular_stocks)
            
            # Remove duplicates and filter
            unique_stocks = self._deduplicate_stocks(stocks)
            filtered_stocks = self._filter_stocks(unique_stocks)
            
            # Cache the results
            self.stocks_cache = filtered_stocks
            self.last_update = datetime.now()
            
            self.logger.info(f"Loaded {len(filtered_stocks)} US stocks")
            return filtered_stocks
            
        except Exception as e:
            self.logger.error(f"Error loading stock database: {e}")
            return self._get_popular_stocks()  # Fallback to popular stocks
    
    def _get_nasdaq_stocks(self) -> List[Dict]:
        """Get NASDAQ listed stocks"""
        try:
            # Load from CSV file
            csv_path = Path(__file__).parent.parent / "data" / "us_stocks.csv"
            
            if csv_path.exists():
                df = pd.read_csv(csv_path)
                nasdaq_stocks = df[df['exchange'] == 'NASDAQ']
                
                return [
                    {
                        'ticker': row['ticker'],
                        'exchange': row['exchange'],
                        'company_name': row['company_name'],
                        'sector': row['sector'],
                        'market_cap_category': row['market_cap_category']
                    }
                    for _, row in nasdaq_stocks.iterrows()
                ]
            else:
                # Fallback to hardcoded list
                nasdaq_stocks = [
                    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX',
                    'ADBE', 'CRM', 'INTC', 'AMD', 'QCOM', 'AVGO', 'CSCO', 'ORCL',
                    'INTU', 'ADP', 'MU', 'KLAC', 'LRCX', 'ADI', 'MCHP', 'SNPS',
                    'CDNS', 'MRVL', 'ASML', 'NXPI', 'TXN', 'SWKS', 'QRVO', 'CRUS',
                    'AMAT', 'TER', 'LSCC', 'XLNX', 'MXL', 'SIMO', 'SYNA', 'IDTI',
                    'CY', 'ON', 'STM', 'NXP'
                ]
                
                return [{'ticker': ticker, 'exchange': 'NASDAQ'} for ticker in nasdaq_stocks]
            
        except Exception as e:
            self.logger.error(f"Error getting NASDAQ stocks: {e}")
            return []
    
    def _get_nyse_stocks(self) -> List[Dict]:
        """Get NYSE listed stocks"""
        try:
            # Load from CSV file
            csv_path = Path(__file__).parent.parent / "data" / "us_stocks.csv"
            
            if csv_path.exists():
                df = pd.read_csv(csv_path)
                nyse_stocks = df[df['exchange'] == 'NYSE']
                
                return [
                    {
                        'ticker': row['ticker'],
                        'exchange': row['exchange'],
                        'company_name': row['company_name'],
                        'sector': row['sector'],
                        'market_cap_category': row['market_cap_category']
                    }
                    for _, row in nyse_stocks.iterrows()
                ]
            else:
                # Fallback to hardcoded list
                nyse_stocks = [
                    'JPM', 'JNJ', 'PG', 'V', 'HD', 'DIS', 'PYPL', 'PFE', 'ABT',
                    'KO', 'PEP', 'TMO', 'COST', 'WMT', 'BAC', 'XOM', 'CVX', 'UNH',
                    'MA', 'MRK', 'LLY', 'T', 'VZ', 'CMCSA', 'ABBV', 'DHR', 'ACN',
                    'NEE', 'UNP', 'RTX', 'HON', 'LOW', 'UPS', 'CAT', 'IBM', 'GS',
                    'MS', 'AXP', 'SPGI', 'PLD', 'SCHW', 'USB', 'BLK', 'DE', 'GE',
                    'MMC', 'TJX', 'COF', 'AON', 'ICE', 'SO', 'DUK', 'D', 'NSC',
                    'EOG', 'SLB', 'COP', 'PSX', 'VLO', 'MPC'
                ]
                
                return [{'ticker': ticker, 'exchange': 'NYSE'} for ticker in nyse_stocks]
            
        except Exception as e:
            self.logger.error(f"Error getting NYSE stocks: {e}")
            return []
    
    def _get_popular_stocks(self) -> List[Dict]:
        """Get popular stocks as fallback"""
        popular_stocks = [
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX',
            'JPM', 'JNJ', 'PG', 'V', 'HD', 'DIS', 'PYPL', 'ADBE', 'CRM',
            'INTC', 'PFE', 'ABT', 'KO', 'PEP', 'TMO', 'AVGO', 'COST',
            'WMT', 'BAC', 'XOM', 'CVX', 'UNH', 'MA', 'MRK', 'LLY', 'T',
            'VZ', 'CMCSA', 'ABBV', 'DHR', 'ACN', 'NEE', 'UNP', 'RTX',
            'HON', 'LOW', 'UPS', 'CAT', 'IBM', 'GS', 'MS', 'AXP', 'SPGI'
        ]
        
        return [{'ticker': ticker, 'exchange': 'UNKNOWN'} for ticker in popular_stocks]
    
    def _deduplicate_stocks(self, stocks: List[Dict]) -> List[Dict]:
        """Remove duplicate stocks"""
        seen = set()
        unique_stocks = []
        
        for stock in stocks:
            ticker = stock['ticker']
            if ticker not in seen:
                seen.add(ticker)
                unique_stocks.append(stock)
        
        return unique_stocks
    
    def _filter_stocks(self, stocks: List[Dict]) -> List[Dict]:
        """Filter stocks based on criteria"""
        filtered = []
        
        for stock in stocks:
            ticker = stock['ticker']
            
            # Basic filtering criteria
            if (len(ticker) <= 5 and  # Reasonable ticker length
                ticker.isalpha() and   # Only letters
                ticker.isupper()):     # All uppercase
                filtered.append(stock)
        
        return filtered
    
    def _is_cache_valid(self) -> bool:
        """Check if cache is still valid"""
        if not self.stocks_cache or not self.last_update:
            return False
        
        time_diff = (datetime.now() - self.last_update).total_seconds()
        return time_diff < self.cache_duration
    
    def search_stocks(self, query: str, limit: int = 50) -> List[Dict]:
        """Search stocks by ticker or company name"""
        try:
            all_stocks = self.get_all_us_stocks()
            
            # Filter by query
            query = query.upper()
            matches = []
            
            for stock in all_stocks:
                ticker = stock['ticker']
                if query in ticker:
                    matches.append(stock)
            
            return matches[:limit]
            
        except Exception as e:
            self.logger.error(f"Error searching stocks: {e}")
            return []
    
    def get_stocks_by_exchange(self, exchange: str) -> List[Dict]:
        """Get stocks by exchange"""
        try:
            all_stocks = self.get_all_us_stocks()
            
            return [stock for stock in all_stocks if stock.get('exchange') == exchange]
            
        except Exception as e:
            self.logger.error(f"Error getting stocks by exchange: {e}")
            return []
    
    def get_stocks_by_market_cap(self, min_cap: float = 0, max_cap: float = float('inf')) -> List[Dict]:
        """Get stocks by market cap range (requires additional API calls)"""
        try:
            all_stocks = self.get_all_us_stocks()
            filtered_stocks = []
            
            for stock in all_stocks:
                try:
                    # Get market cap for each stock
                    ticker = yf.Ticker(stock['ticker'])
                    market_cap = ticker.info.get('marketCap', 0)
                    
                    if min_cap <= market_cap <= max_cap:
                        stock['market_cap'] = market_cap
                        filtered_stocks.append(stock)
                    
                    # Rate limiting
                    time.sleep(0.1)
                    
                except Exception as e:
                    self.logger.debug(f"Error getting market cap for {stock['ticker']}: {e}")
                    continue
            
            return filtered_stocks
            
        except Exception as e:
            self.logger.error(f"Error filtering by market cap: {e}")
            return []
    
    def get_total_stock_count(self) -> int:
        """Get total number of stocks in database"""
        try:
            all_stocks = self.get_all_us_stocks()
            return len(all_stocks)
        except Exception as e:
            self.logger.error(f"Error getting stock count: {e}")
            return 0 