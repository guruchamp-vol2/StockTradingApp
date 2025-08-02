import yfinance as yf
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import ta
from datetime import datetime, timedelta
import logging

from config import Config
from utils.stock_database import StockDatabase

class StockAnalyzer:
    """Comprehensive stock analysis using fundamental and technical indicators"""
    
    def __init__(self):
        self.config = Config()
        self.stock_db = StockDatabase()
        logging.basicConfig(level=getattr(logging, self.config.LOG_LEVEL))
        self.logger = logging.getLogger(__name__)
    
    def get_stock_data(self, ticker: str, period: str = "1y") -> Optional[yf.Ticker]:
        """Fetch stock data from Yahoo Finance"""
        try:
            stock = yf.Ticker(ticker)
            # Test if data is available
            info = stock.info
            if info.get('regularMarketPrice') is None:
                return None
            return stock
        except Exception as e:
            self.logger.error(f"Error fetching data for {ticker}: {e}")
            return None
    
    def calculate_fundamental_score(self, stock: yf.Ticker) -> Dict:
        """Calculate fundamental analysis score based on Motley Fool principles"""
        try:
            info = stock.info
            
            # Basic financial metrics
            market_cap = info.get('marketCap', 0)
            pe_ratio = info.get('trailingPE', 0)
            pb_ratio = info.get('priceToBook', 0)
            debt_to_equity = info.get('debtToEquity', 0)
            roe = info.get('returnOnEquity', 0)
            revenue_growth = info.get('revenueGrowth', 0)
            profit_margins = info.get('profitMargins', 0)
            
            # Calculate fundamental score (0-100)
            score = 0
            reasons = []
            
            # Market cap filter (prefer larger companies)
            if market_cap >= self.config.MIN_MARKET_CAP:
                score += 15
                reasons.append("Large market cap (>$1B)")
            elif market_cap >= 500000000:  # $500M
                score += 10
                reasons.append("Mid-cap stock")
            
            # P/E ratio analysis
            if pe_ratio and pe_ratio > 0 and pe_ratio <= self.config.MAX_PE_RATIO:
                score += 15
                reasons.append(f"Reasonable P/E ratio ({pe_ratio:.2f})")
            elif pe_ratio and pe_ratio > 0:
                score += 5
                reasons.append(f"High P/E ratio ({pe_ratio:.2f})")
            
            # ROE analysis
            if roe and roe >= self.config.MIN_ROE:
                score += 20
                reasons.append(f"Strong ROE ({roe:.2%})")
            elif roe and roe > 0:
                score += 10
                reasons.append(f"Positive ROE ({roe:.2%})")
            
            # Debt analysis
            if debt_to_equity and debt_to_equity <= 0.5:
                score += 15
                reasons.append("Low debt levels")
            elif debt_to_equity and debt_to_equity <= 1.0:
                score += 10
                reasons.append("Moderate debt levels")
            
            # Revenue growth
            if revenue_growth and revenue_growth > 0.1:
                score += 15
                reasons.append(f"Strong revenue growth ({revenue_growth:.2%})")
            elif revenue_growth and revenue_growth > 0:
                score += 10
                reasons.append(f"Positive revenue growth ({revenue_growth:.2%})")
            
            # Profit margins
            if profit_margins and profit_margins > 0.15:
                score += 10
                reasons.append(f"High profit margins ({profit_margins:.2%})")
            elif profit_margins and profit_margins > 0:
                score += 5
                reasons.append(f"Positive profit margins ({profit_margins:.2%})")
            
            # Additional checks
            if info.get('beta', 0) < 1.2:
                score += 5
                reasons.append("Lower volatility than market")
            
            return {
                'score': min(score, 100),
                'reasons': reasons,
                'metrics': {
                    'market_cap': market_cap,
                    'pe_ratio': pe_ratio,
                    'pb_ratio': pb_ratio,
                    'debt_to_equity': debt_to_equity,
                    'roe': roe,
                    'revenue_growth': revenue_growth,
                    'profit_margins': profit_margins,
                    'beta': info.get('beta', 0)
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error in fundamental analysis: {e}")
            return {'score': 0, 'reasons': ['Error in analysis'], 'metrics': {}}
    
    def calculate_technical_score(self, stock: yf.Ticker) -> Dict:
        """Calculate technical analysis score"""
        try:
            # Get historical data
            hist = stock.history(period="6mo")
            if hist.empty:
                return {'score': 0, 'reasons': ['Insufficient data'], 'indicators': {}}
            
            # Calculate technical indicators
            indicators = {}
            
            # RSI
            rsi = ta.momentum.RSIIndicator(hist['Close']).rsi()
            current_rsi = rsi.iloc[-1]
            indicators['rsi'] = current_rsi
            
            # Moving averages
            ma_20 = ta.trend.SMAIndicator(hist['Close'], window=20).sma_indicator()
            ma_50 = ta.trend.SMAIndicator(hist['Close'], window=50).sma_indicator()
            current_price = hist['Close'].iloc[-1]
            current_ma20 = ma_20.iloc[-1]
            current_ma50 = ma_50.iloc[-1]
            
            indicators['ma_20'] = current_ma20
            indicators['ma_50'] = current_ma50
            indicators['price_vs_ma20'] = (current_price / current_ma20 - 1) * 100
            indicators['price_vs_ma50'] = (current_price / current_ma50 - 1) * 100
            
            # MACD
            macd = ta.trend.MACD(hist['Close'])
            macd_line = macd.macd()
            signal_line = macd.macd_signal()
            indicators['macd'] = macd_line.iloc[-1]
            indicators['macd_signal'] = signal_line.iloc[-1]
            
            # Bollinger Bands
            bb = ta.volatility.BollingerBands(hist['Close'])
            bb_upper = bb.bollinger_hband()
            bb_lower = bb.bollinger_lband()
            indicators['bb_position'] = (current_price - bb_lower.iloc[-1]) / (bb_upper.iloc[-1] - bb_lower.iloc[-1])
            
            # Volume analysis
            avg_volume = hist['Volume'].mean()
            current_volume = hist['Volume'].iloc[-1]
            indicators['volume_ratio'] = current_volume / avg_volume
            
            # Calculate technical score
            score = 0
            reasons = []
            
            # RSI analysis
            if current_rsi < self.config.RSI_OVERSOLD:
                score += 15
                reasons.append("Oversold (RSI < 30)")
            elif current_rsi < 45:
                score += 10
                reasons.append("Neutral RSI")
            elif current_rsi > self.config.RSI_OVERBOUGHT:
                score += 5
                reasons.append("Overbought (RSI > 70)")
            
            # Moving average analysis
            if current_price > current_ma20 and current_ma20 > current_ma50:
                score += 20
                reasons.append("Strong uptrend (price > MA20 > MA50)")
            elif current_price > current_ma20:
                score += 15
                reasons.append("Price above 20-day MA")
            elif current_price > current_ma50:
                score += 10
                reasons.append("Price above 50-day MA")
            
            # MACD analysis
            if macd_line.iloc[-1] > signal_line.iloc[-1]:
                score += 15
                reasons.append("Positive MACD crossover")
            
            # Volume analysis
            if indicators['volume_ratio'] > 1.5:
                score += 10
                reasons.append("High volume (1.5x average)")
            elif indicators['volume_ratio'] > 1.0:
                score += 5
                reasons.append("Above average volume")
            
            # Bollinger Bands analysis
            if indicators['bb_position'] < 0.2:
                score += 10
                reasons.append("Near lower Bollinger Band")
            elif indicators['bb_position'] > 0.8:
                score += 5
                reasons.append("Near upper Bollinger Band")
            
            return {
                'score': min(score, 100),
                'reasons': reasons,
                'indicators': indicators
            }
            
        except Exception as e:
            self.logger.error(f"Error in technical analysis: {e}")
            return {'score': 0, 'reasons': ['Error in analysis'], 'indicators': {}}
    
    def get_stock_recommendation(self, ticker: str) -> Dict:
        """Get comprehensive stock recommendation"""
        stock = self.get_stock_data(ticker)
        if not stock:
            return {
                'ticker': ticker,
                'error': 'Unable to fetch stock data',
                'recommendation': 'SKIP',
                'overall_score': 0
            }
        
        # Get fundamental and technical scores
        fundamental = self.calculate_fundamental_score(stock)
        technical = self.calculate_technical_score(stock)
        
        # Calculate weighted overall score
        overall_score = (
            fundamental['score'] * self.config.FUNDAMENTAL_WEIGHT +
            technical['score'] * self.config.TECHNICAL_WEIGHT
        )
        
        # Determine recommendation
        if overall_score >= 80:
            recommendation = "STRONG_BUY"
        elif overall_score >= 60:
            recommendation = "BUY"
        elif overall_score >= 40:
            recommendation = "HOLD"
        elif overall_score >= 20:
            recommendation = "SELL"
        else:
            recommendation = "STRONG_SELL"
        
        return {
            'ticker': ticker,
            'overall_score': round(overall_score, 2),
            'fundamental_score': fundamental['score'],
            'technical_score': technical['score'],
            'recommendation': recommendation,
            'fundamental_reasons': fundamental['reasons'],
            'technical_reasons': technical['reasons'],
            'fundamental_metrics': fundamental['metrics'],
            'technical_indicators': technical['indicators'],
            'current_price': stock.info.get('regularMarketPrice', 0),
            'market_cap': stock.info.get('marketCap', 0),
            'volume': stock.info.get('volume', 0)
        }
    
    def screen_stocks(self, criteria: Dict) -> List[Dict]:
        """Screen stocks based on criteria using comprehensive database"""
        try:
            # Get all stocks from database
            all_stocks = self.stock_db.get_all_us_stocks()
            self.logger.info(f"Screening {len(all_stocks)} stocks...")
            
            results = []
            processed = 0
            
            for stock_info in all_stocks:
                ticker = stock_info['ticker']
                processed += 1
                
                # Progress indicator
                if processed % 10 == 0:
                    self.logger.info(f"Processed {processed}/{len(all_stocks)} stocks...")
                
                try:
                    result = self.get_stock_recommendation(ticker)
                    if result.get('error'):
                        continue
                    
                    # Apply filters
                    if criteria.get('min_score', 0) <= result['overall_score'] <= criteria.get('max_score', 100):
                        if result['market_cap'] >= criteria.get('min_market_cap', 0):
                            # Add exchange info
                            result['exchange'] = stock_info.get('exchange', 'UNKNOWN')
                            results.append(result)
                    
                    # Limit results to avoid overwhelming
                    if len(results) >= criteria.get('max_results', 100):
                        break
                        
                except Exception as e:
                    self.logger.debug(f"Error screening {ticker}: {e}")
                    continue
            
            # Sort by overall score
            results.sort(key=lambda x: x['overall_score'], reverse=True)
            
            self.logger.info(f"Screening complete. Found {len(results)} matching stocks.")
            return results
            
        except Exception as e:
            self.logger.error(f"Error in stock screening: {e}")
            return []
    
    def get_stock_count(self) -> int:
        """Get total number of stocks available for screening"""
        return self.stock_db.get_total_stock_count()
    
    def search_stocks(self, query: str, limit: int = 50) -> List[Dict]:
        """Search stocks by ticker or company name"""
        return self.stock_db.search_stocks(query, limit)
    
    def get_stocks_by_exchange(self, exchange: str) -> List[Dict]:
        """Get stocks by exchange"""
        return self.stock_db.get_stocks_by_exchange(exchange)
    
    def get_stocks_by_market_cap(self, min_cap: float = 0, max_cap: float = float('inf')) -> List[Dict]:
        """Get stocks by market cap range"""
        return self.stock_db.get_stocks_by_market_cap(min_cap, max_cap) 
import yfinance as yf
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging
import time
import ta

from config import Config
from utils.stock_database import StockDatabase

class StockAnalyzer:
    def __init__(self):
        self.config = Config()
        self.stock_db = StockDatabase()
        logging.basicConfig(level=getattr(logging, self.config.LOG_LEVEL))
        self.logger = logging.getLogger(__name__)

    def get_stock_data(self, ticker: str, period: str = "1y", retries: int = 3, delay: float = 2.0) -> Optional[yf.Ticker]:
        """Fetch stock data with retries and exponential backoff."""
        for attempt in range(retries):
            try:
                stock = yf.Ticker(ticker)
                info = stock.info
                if info.get('regularMarketPrice') is None:
                    return None
                return stock
            except Exception as e:
                self.logger.warning(f"[{ticker}] Attempt {attempt+1} failed: {e}")
                time.sleep(delay * (2 ** attempt))
        return None

    def calculate_fundamental_score(self, stock: yf.Ticker) -> Dict:
        try:
            info = stock.info
            score = 0
            reasons = []

            market_cap = info.get('marketCap', 0)
            pe_ratio = info.get('trailingPE')
            pb_ratio = info.get('priceToBook')
            debt_to_equity = info.get('debtToEquity')
            roe = info.get('returnOnEquity')
            revenue_growth = info.get('revenueGrowth')
            profit_margins = info.get('profitMargins')

            if market_cap >= self.config.MIN_MARKET_CAP:
                score += 15
                reasons.append("Large cap company")
            elif market_cap >= 500_000_000:
                score += 10
                reasons.append("Mid cap company")

            if pe_ratio and 0 < pe_ratio <= self.config.MAX_PE_RATIO:
                score += 15
                reasons.append(f"Fair P/E ({pe_ratio:.2f})")
            elif pe_ratio and pe_ratio > self.config.MAX_PE_RATIO:
                score += 5
                reasons.append(f"High P/E ({pe_ratio:.2f})")

            if roe and roe >= self.config.MIN_ROE:
                score += 20
                reasons.append(f"Strong ROE ({roe:.2%})")
            elif roe:
                score += 10
                reasons.append(f"Positive ROE ({roe:.2%})")

            if debt_to_equity is not None:
                if debt_to_equity <= 0.5:
                    score += 15
                    reasons.append("Low debt")
                elif debt_to_equity <= 1.0:
                    score += 10
                    reasons.append("Moderate debt")

            if revenue_growth:
                if revenue_growth > 0.1:
                    score += 15
                    reasons.append(f"Strong revenue growth ({revenue_growth:.2%})")
                elif revenue_growth > 0:
                    score += 10
                    reasons.append(f"Positive revenue growth ({revenue_growth:.2%})")

            if profit_margins:
                if profit_margins > 0.15:
                    score += 10
                    reasons.append(f"High profit margins ({profit_margins:.2%})")
                elif profit_margins > 0:
                    score += 5
                    reasons.append(f"Positive profit margins ({profit_margins:.2%})")

            if info.get('beta', 0) < 1.2:
                score += 5
                reasons.append("Lower volatility")

            return {
                'score': min(score, 100),
                'reasons': reasons,
                'metrics': {
                    'market_cap': market_cap,
                    'pe_ratio': pe_ratio,
                    'pb_ratio': pb_ratio,
                    'debt_to_equity': debt_to_equity,
                    'roe': roe,
                    'revenue_growth': revenue_growth,
                    'profit_margins': profit_margins,
                    'beta': info.get('beta', 0)
                }
            }

        except Exception as e:
            self.logger.error(f"Error in fundamental analysis: {e}")
            return {'score': 0, 'reasons': ['Error in fundamental analysis'], 'metrics': {}}

    def calculate_technical_score(self, stock: yf.Ticker) -> Dict:
        try:
            hist = stock.history(period="6mo")
            if hist.empty:
                return {'score': 0, 'reasons': ['No historical data'], 'indicators': {}}

            indicators = {}
            price = hist['Close']

            rsi = ta.momentum.RSIIndicator(close=price).rsi().iloc[-1]
            ma20 = price.rolling(window=20).mean().iloc[-1]
            ma50 = price.rolling(window=50).mean().iloc[-1]
            current_price = price.iloc[-1]

            indicators.update({
                'rsi': rsi,
                'ma_20': ma20,
                'ma_50': ma50,
                'price_vs_ma20': (current_price / ma20 - 1) * 100,
                'price_vs_ma50': (current_price / ma50 - 1) * 100
            })

            macd = ta.trend.MACD(close=price)
            indicators['macd'] = macd.macd().iloc[-1]
            indicators['macd_signal'] = macd.macd_signal().iloc[-1]

            bb = ta.volatility.BollingerBands(close=price)
            indicators['bb_position'] = (
                (current_price - bb.bollinger_lband().iloc[-1]) /
                (bb.bollinger_hband().iloc[-1] - bb.bollinger_lband().iloc[-1])
            )

            volume = hist['Volume']
            indicators['volume_ratio'] = volume.iloc[-1] / volume.mean()

            score = 0
            reasons = []

            if rsi < 30:
                score += 15
                reasons.append("Oversold RSI")
            elif rsi < 45:
                score += 10
                reasons.append("Weak RSI")
            elif rsi > 70:
                score += 5
                reasons.append("Overbought RSI")

            if current_price > ma20 and ma20 > ma50:
                score += 20
                reasons.append("Strong uptrend")
            elif current_price > ma20:
                score += 10
                reasons.append("Price above MA20")

            if indicators['macd'] > indicators['macd_signal']:
                score += 15
                reasons.append("Positive MACD crossover")

            if indicators['volume_ratio'] > 1.5:
                score += 10
                reasons.append("High volume")
            elif indicators['volume_ratio'] > 1.0:
                score += 5
                reasons.append("Above average volume")

            if indicators['bb_position'] < 0.2:
                score += 10
                reasons.append("Near lower Bollinger Band")
            elif indicators['bb_position'] > 0.8:
                score += 5
                reasons.append("Near upper Bollinger Band")

            return {
                'score': min(score, 100),
                'reasons': reasons,
                'indicators': indicators
            }

        except Exception as e:
            self.logger.error(f"Error in technical analysis: {e}")
            return {'score': 0, 'reasons': ['Error in technical analysis'], 'indicators': {}}

    def get_stock_recommendation(self, ticker: str) -> Dict:
        stock = self.get_stock_data(ticker)
        if not stock:
            return {
                'ticker': ticker,
                'error': 'Unable to fetch stock data',
                'recommendation': 'SKIP',
                'overall_score': 0
            }

        fundamental = self.calculate_fundamental_score(stock)
        technical = self.calculate_technical_score(stock)

        overall_score = (
            fundamental['score'] * self.config.FUNDAMENTAL_WEIGHT +
            technical['score'] * self.config.TECHNICAL_WEIGHT
        )

        if overall_score >= 80:
            recommendation = "STRONG_BUY"
        elif overall_score >= 60:
            recommendation = "BUY"
        elif overall_score >= 40:
            recommendation = "HOLD"
        elif overall_score >= 20:
            recommendation = "SELL"
        else:
            recommendation = "STRONG_SELL"

        return {
            'ticker': ticker,
            'overall_score': round(overall_score, 2),
            'fundamental_score': fundamental['score'],
            'technical_score': technical['score'],
            'recommendation': recommendation,
            'fundamental_reasons': fundamental['reasons'],
            'technical_reasons': technical['reasons'],
            'fundamental_metrics': fundamental['metrics'],
            'technical_indicators': technical['indicators'],
            'current_price': stock.info.get('regularMarketPrice', 0),
            'market_cap': stock.info.get('marketCap', 0),
            'volume': stock.info.get('volume', 0)
        }

    def screen_stocks(self, criteria: Dict) -> List[Dict]:
        all_stocks = self.stock_db.get_all_us_stocks()
        results = []

        for stock_info in all_stocks:
            ticker = stock_info['ticker']
            try:
                result = self.get_stock_recommendation(ticker)
                if result.get('error'):
                    continue
                if (criteria['min_score'] <= result['overall_score'] <= criteria['max_score'] and
                    result['market_cap'] >= criteria['min_market_cap']):
                    result['exchange'] = stock_info.get('exchange', 'UNKNOWN')
                    results.append(result)
                if len(results) >= criteria.get('max_results', 100):
                    break
            except Exception:
                continue

        results.sort(key=lambda x: x['overall_score'], reverse=True)
        return results

    def get_stock_count(self) -> int:
        return self.stock_db.get_total_stock_count()

    def search_stocks(self, query: str, limit: int = 50) -> List[Dict]:
        return self.stock_db.search_stocks(query, limit)

    def get_stocks_by_exchange(self, exchange: str) -> List[Dict]:
        return self.stock_db.get_stocks_by_exchange(exchange)

    def get_stocks_by_market_cap(self, min_cap: float = 0, max_cap: float = float('inf')) -> List[Dict]:
        return self.stock_db.get_stocks_by_market_cap(min_cap, max_cap)
