import requests
import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging
from textblob import TextBlob
import json

from config import Config

class NewsAnalyzer:
    """Analyze financial news and sentiment for stocks"""
    
    def __init__(self):
        self.config = Config()
        self.logger = logging.getLogger(__name__)
        self.news_api_key = self.config.NEWS_API_KEY
        
    def get_stock_news(self, ticker: str, days: int = 7) -> List[Dict]:
        """Fetch news articles for a specific stock"""
        if not self.news_api_key:
            return self._get_sample_news(ticker)
        
        try:
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # News API query
            url = "https://newsapi.org/v2/everything"
            params = {
                'q': f'"{ticker}" OR "{ticker} stock" OR "{ticker} shares"',
                'from': start_date.strftime('%Y-%m-%d'),
                'to': end_date.strftime('%Y-%m-%d'),
                'language': 'en',
                'sortBy': 'publishedAt',
                'apiKey': self.news_api_key
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            articles = data.get('articles', [])
            
            # Process articles
            processed_articles = []
            for article in articles:
                processed_articles.append({
                    'title': article.get('title', ''),
                    'description': article.get('description', ''),
                    'url': article.get('url', ''),
                    'published_at': article.get('publishedAt', ''),
                    'source': article.get('source', {}).get('name', ''),
                    'sentiment': self._analyze_sentiment(article.get('title', '') + ' ' + article.get('description', ''))
                })
            
            return processed_articles
            
        except Exception as e:
            self.logger.error(f"Error fetching news for {ticker}: {e}")
            return self._get_sample_news(ticker)
    
    def _analyze_sentiment(self, text: str) -> Dict:
        """Analyze sentiment of text using TextBlob"""
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            
            # Categorize sentiment
            if polarity > 0.1:
                sentiment = 'positive'
            elif polarity < -0.1:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            
            return {
                'polarity': polarity,
                'subjectivity': subjectivity,
                'sentiment': sentiment
            }
        except Exception as e:
            self.logger.error(f"Error analyzing sentiment: {e}")
            return {
                'polarity': 0,
                'subjectivity': 0,
                'sentiment': 'neutral'
            }
    
    def get_market_news(self, days: int = 7) -> List[Dict]:
        """Fetch general market news"""
        if not self.news_api_key:
            return self._get_sample_market_news()
        
        try:
            url = "https://newsapi.org/v2/top-headlines"
            params = {
                'category': 'business',
                'language': 'en',
                'apiKey': self.news_api_key
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            articles = data.get('articles', [])
            
            processed_articles = []
            for article in articles:
                processed_articles.append({
                    'title': article.get('title', ''),
                    'description': article.get('description', ''),
                    'url': article.get('url', ''),
                    'published_at': article.get('publishedAt', ''),
                    'source': article.get('source', {}).get('name', ''),
                    'sentiment': self._analyze_sentiment(article.get('title', '') + ' ' + article.get('description', ''))
                })
            
            return processed_articles
            
        except Exception as e:
            self.logger.error(f"Error fetching market news: {e}")
            return self._get_sample_market_news()
    
    def calculate_news_sentiment_score(self, articles: List[Dict]) -> Dict:
        """Calculate overall sentiment score from articles"""
        if not articles:
            return {
                'score': 0,
                'sentiment': 'neutral',
                'article_count': 0,
                'positive_count': 0,
                'negative_count': 0,
                'neutral_count': 0
            }
        
        total_polarity = 0
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        
        for article in articles:
            sentiment = article.get('sentiment', {})
            polarity = sentiment.get('polarity', 0)
            sentiment_type = sentiment.get('sentiment', 'neutral')
            
            total_polarity += polarity
            
            if sentiment_type == 'positive':
                positive_count += 1
            elif sentiment_type == 'negative':
                negative_count += 1
            else:
                neutral_count += 1
        
        avg_polarity = total_polarity / len(articles)
        
        # Convert to 0-100 score
        sentiment_score = (avg_polarity + 1) * 50  # Convert from -1,1 to 0,100
        
        # Determine overall sentiment
        if sentiment_score > 60:
            overall_sentiment = 'positive'
        elif sentiment_score < 40:
            overall_sentiment = 'negative'
        else:
            overall_sentiment = 'neutral'
        
        return {
            'score': round(sentiment_score, 2),
            'sentiment': overall_sentiment,
            'article_count': len(articles),
            'positive_count': positive_count,
            'negative_count': negative_count,
            'neutral_count': neutral_count,
            'avg_polarity': round(avg_polarity, 3)
        }
    
    def _get_sample_news(self, ticker: str) -> List[Dict]:
        """Return sample news when API is not available"""
        sample_news = [
            {
                'title': f'{ticker} Reports Strong Q4 Earnings',
                'description': f'{ticker} exceeded analyst expectations with strong quarterly results.',
                'url': '#',
                'published_at': datetime.now().isoformat(),
                'source': 'Financial News',
                'sentiment': {'polarity': 0.3, 'subjectivity': 0.6, 'sentiment': 'positive'}
            },
            {
                'title': f'{ticker} Announces New Product Launch',
                'description': f'{ticker} unveiled innovative new products at annual conference.',
                'url': '#',
                'published_at': datetime.now().isoformat(),
                'source': 'Market Watch',
                'sentiment': {'polarity': 0.2, 'subjectivity': 0.5, 'sentiment': 'positive'}
            },
            {
                'title': f'{ticker} Faces Regulatory Challenges',
                'description': f'{ticker} encounters regulatory hurdles in key markets.',
                'url': '#',
                'published_at': datetime.now().isoformat(),
                'source': 'Business Daily',
                'sentiment': {'polarity': -0.1, 'subjectivity': 0.4, 'sentiment': 'neutral'}
            }
        ]
        return sample_news
    
    def _get_sample_market_news(self) -> List[Dict]:
        """Return sample market news when API is not available"""
        sample_news = [
            {
                'title': 'Federal Reserve Maintains Interest Rates',
                'description': 'The Fed keeps rates steady, signaling continued economic stability.',
                'url': '#',
                'published_at': datetime.now().isoformat(),
                'source': 'Financial Times',
                'sentiment': {'polarity': 0.1, 'subjectivity': 0.3, 'sentiment': 'neutral'}
            },
            {
                'title': 'Tech Stocks Rally on Strong Earnings',
                'description': 'Technology sector sees broad gains following positive earnings reports.',
                'url': '#',
                'published_at': datetime.now().isoformat(),
                'source': 'Market Watch',
                'sentiment': {'polarity': 0.4, 'subjectivity': 0.5, 'sentiment': 'positive'}
            },
            {
                'title': 'Oil Prices Decline on Supply Concerns',
                'description': 'Crude oil prices fall amid global supply chain issues.',
                'url': '#',
                'published_at': datetime.now().isoformat(),
                'source': 'Reuters',
                'sentiment': {'polarity': -0.2, 'subjectivity': 0.4, 'sentiment': 'negative'}
            }
        ]
        return sample_news 