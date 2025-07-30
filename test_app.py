#!/usr/bin/env python3
"""
Test script for AI Stock Analyzer & Advisor
"""

import sys
import os
from pathlib import Path

# Add the project root to the path
sys.path.append(str(Path(__file__).parent))

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        from utils.stock_analyzer import StockAnalyzer
        from utils.news_analyzer import NewsAnalyzer
        from utils.ai_advisor import AIAdvisor
        from config import Config
        print("✅ All modules imported successfully!")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_stock_analyzer():
    """Test stock analyzer functionality"""
    print("\n🧪 Testing Stock Analyzer...")
    
    try:
        from utils.stock_analyzer import StockAnalyzer
        
        analyzer = StockAnalyzer()
        
        # Test with a well-known stock
        result = analyzer.get_stock_recommendation("AAPL")
        
        if result and not result.get('error'):
            print("✅ Stock analyzer working!")
            print(f"   - Ticker: {result.get('ticker')}")
            print(f"   - Score: {result.get('overall_score')}/100")
            print(f"   - Recommendation: {result.get('recommendation')}")
            return True
        else:
            print("❌ Stock analyzer failed to get data")
            return False
            
    except Exception as e:
        print(f"❌ Stock analyzer error: {e}")
        return False

def test_news_analyzer():
    """Test news analyzer functionality"""
    print("\n🧪 Testing News Analyzer...")
    
    try:
        from utils.news_analyzer import NewsAnalyzer
        
        analyzer = NewsAnalyzer()
        
        # Test market news
        news = analyzer.get_market_news(days=1)
        
        if news:
            print("✅ News analyzer working!")
            print(f"   - Found {len(news)} articles")
            
            # Test sentiment analysis
            sentiment = analyzer.calculate_news_sentiment_score(news)
            print(f"   - Sentiment score: {sentiment.get('score')}/100")
            return True
        else:
            print("❌ News analyzer failed to get data")
            return False
            
    except Exception as e:
        print(f"❌ News analyzer error: {e}")
        return False

def test_ai_advisor():
    """Test AI advisor functionality"""
    print("\n🧪 Testing AI Advisor...")
    
    try:
        from utils.ai_advisor import AIAdvisor
        
        advisor = AIAdvisor()
        
        # Test with sample data
        sample_stock_data = {
            'ticker': 'AAPL',
            'current_price': 175.43,
            'overall_score': 85,
            'recommendation': 'STRONG_BUY',
            'fundamental_score': 88,
            'technical_score': 82
        }
        
        sample_news = [
            {
                'title': 'Apple Reports Strong Earnings',
                'sentiment': {'sentiment': 'positive'}
            }
        ]
        
        analysis = advisor.get_stock_analysis(sample_stock_data, sample_news)
        
        if analysis:
            print("✅ AI advisor working!")
            print(f"   - Analysis generated for {analysis.get('ticker')}")
            return True
        else:
            print("❌ AI advisor failed to generate analysis")
            return False
            
    except Exception as e:
        print(f"❌ AI advisor error: {e}")
        return False

def test_config():
    """Test configuration loading"""
    print("\n🧪 Testing Configuration...")
    
    try:
        from config import Config
        
        config = Config()
        
        print("✅ Configuration loaded!")
        print(f"   - Debug mode: {config.DEBUG}")
        print(f"   - Log level: {config.LOG_LEVEL}")
        print(f"   - Min market cap: ${config.MIN_MARKET_CAP:,.0f}")
        return True
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_dependencies():
    """Test if all required packages are installed"""
    print("\n🧪 Testing Dependencies...")
    
    required_packages = [
        'streamlit', 'pandas', 'numpy', 'yfinance', 'requests',
        'beautifulsoup4', 'plotly', 'openai', 'python-dotenv',
        'newsapi-python', 'textblob', 'scikit-learn', 'ta'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("   Run: pip install -r requirements.txt")
        return False
    else:
        print("✅ All required packages installed!")
        return True

def main():
    """Run all tests"""
    print("🚀 Testing AI Stock Analyzer & Advisor")
    print("=" * 50)
    
    tests = [
        test_dependencies,
        test_imports,
        test_config,
        test_stock_analyzer,
        test_news_analyzer,
        test_ai_advisor
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The app is ready to run.")
        print("\n📋 Next steps:")
        print("1. Configure API keys in .env file")
        print("2. Run: python run.py")
        print("3. Or run: streamlit run app.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\n🔧 Troubleshooting:")
        print("1. Install missing packages: pip install -r requirements.txt")
        print("2. Check your internet connection")
        print("3. Verify API keys are configured")
    
    print("\n⚠️  Remember: This app is for educational purposes only!")

if __name__ == "__main__":
    main() 