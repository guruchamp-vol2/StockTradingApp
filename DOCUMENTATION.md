# AI Stock Analyzer & Advisor - Documentation

## 📋 Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Usage](#usage)
6. [Investment Philosophy](#investment-philosophy)
7. [API Reference](#api-reference)
8. [Troubleshooting](#troubleshooting)
9. [Disclaimer](#disclaimer)

## 🎯 Overview

The AI Stock Analyzer & Advisor is a comprehensive stock analysis application that combines fundamental analysis, technical indicators, news sentiment analysis, and AI-powered insights to help users make informed investment decisions.

The app follows **The Motley Fool's 8-step investment process** and incorporates proven investment strategies from credible sources.

## 🚀 Features

### 📊 Smart Stock Recommendations
- **Fundamental Analysis**: P/E ratios, debt-to-equity, ROE, revenue growth
- **Technical Analysis**: Moving averages, RSI, MACD, volume analysis
- **Competitive Advantages**: Business model analysis using Motley Fool principles
- **Risk Assessment**: Comprehensive risk evaluation for each stock

### 📈 Real-time Data & Analysis
- **Live Stock Data**: Real-time prices, volume, market cap
- **Financial Statements**: Income statements, balance sheets, cash flow
- **Technical Indicators**: 20+ technical indicators for each stock
- **Market Sentiment**: News sentiment analysis and social media trends

### 📰 News Integration
- **Real-time News**: Latest financial news from multiple sources
- **Sentiment Analysis**: AI-powered news sentiment scoring
- **Market Trends**: Sector-specific news and analysis

### 🤖 AI-Powered Insights
- **Stock Scoring**: Multi-factor scoring system (0-100)
- **Recommendation Engine**: Personalized recommendations based on risk profile
- **Portfolio Analysis**: Diversification and risk assessment
- **Market Timing**: Entry/exit point suggestions

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Start
1. **Clone the repository**
```bash
git clone <repository-url>
cd StockTradingApp
```

2. **Run the setup script**
```bash
python setup.py
```

3. **Configure API keys**
Edit the `.env` file with your API keys:
```env
OPENAI_API_KEY=your_openai_api_key_here
NEWS_API_KEY=your_news_api_key_here
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key_here
```

4. **Start the application**
```bash
python run.py
# or
streamlit run app.py
```

### Manual Installation
If you prefer manual installation:

1. **Install dependencies**
```bash
pip install -r requirements.txt
```

2. **Create .env file**
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. **Run the app**
```bash
streamlit run app.py
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `OPENAI_API_KEY` | OpenAI API key for AI insights | Yes | - |
| `NEWS_API_KEY` | News API key for financial news | No | - |
| `ALPHA_VANTAGE_API_KEY` | Alpha Vantage API key | No | - |
| `DEBUG` | Enable debug mode | No | True |
| `LOG_LEVEL` | Logging level | No | INFO |

### App Settings (config.py)

| Setting | Description | Default |
|---------|-------------|---------|
| `MIN_MARKET_CAP` | Minimum market cap for screening | $1B |
| `MIN_VOLUME` | Minimum volume for screening | 1M |
| `MAX_PE_RATIO` | Maximum P/E ratio for value stocks | 50 |
| `MIN_ROE` | Minimum ROE for quality stocks | 10% |
| `RSI_OVERSOLD` | RSI oversold threshold | 30 |
| `RSI_OVERBOUGHT` | RSI overbought threshold | 70 |

## 📖 Usage

### 🏠 Dashboard
The main dashboard provides:
- Market overview with key indices
- Top stock recommendations
- Latest market news
- Quick access to all features

### 🔍 Stock Analysis
1. **Enter a stock ticker** (e.g., AAPL, MSFT, GOOGL)
2. **Click "Analyze Stock"**
3. **Review the comprehensive analysis**:
   - Fundamental metrics
   - Technical indicators
   - News sentiment
   - AI-powered insights

### 📰 Market News
- View latest financial news
- Analyze market sentiment
- Get AI-powered market insights
- Track sector-specific trends

### 📈 Stock Screener
1. **Set screening criteria**:
   - Minimum/maximum score
   - Market cap range
   - Recommendation filter
2. **Run the screener**
3. **Review results** and download data

### 💼 Portfolio Tracker
1. **Add stocks to your portfolio**
2. **Track performance** and metrics
3. **Get AI portfolio analysis**
4. **Monitor diversification** and risk

## 🎯 Investment Philosophy

The app follows **The Motley Fool's 8-Step Process**:

### 1. Understand the Business Model
- Invest in companies you understand
- Focus on clear, sustainable business models
- Avoid complex financial instruments

### 2. Look for Competitive Advantages
- **Economic moats**: Network effects, switching costs
- **Cost advantages**: Scale, efficiency, technology
- **Intangible assets**: Brand, patents, licenses

### 3. Dig into the Numbers
- **P/E Ratio**: Price relative to earnings
- **ROE**: Return on equity efficiency
- **Debt Levels**: Financial health indicator
- **Growth Metrics**: Revenue and earnings growth

### 4. Prove Yourself Wrong
- Challenge your investment thesis
- Consider what could go wrong
- Get input from different perspectives

### 5. Learn to Say "No"
- Be selective about investments
- Quality over quantity
- Avoid FOMO (Fear of Missing Out)

### 6. Learn from Mistakes
- Keep an investment journal
- Review decisions regularly
- Understand what went wrong

### 7. Learn from Successes
- Study winning investments
- Identify patterns
- Build on successful strategies

### 8. Invest in Knowledge
- Continuous learning
- Stay updated on markets
- Develop expertise over time

## 🔧 API Reference

### StockAnalyzer Class

#### Methods

##### `get_stock_data(ticker: str, period: str = "1y")`
Fetch stock data from Yahoo Finance.

**Parameters:**
- `ticker`: Stock symbol (e.g., "AAPL")
- `period`: Data period ("1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max")

**Returns:** yf.Ticker object or None

##### `calculate_fundamental_score(stock: yf.Ticker)`
Calculate fundamental analysis score (0-100).

**Parameters:**
- `stock`: yf.Ticker object

**Returns:** Dict with score, reasons, and metrics

##### `calculate_technical_score(stock: yf.Ticker)`
Calculate technical analysis score (0-100).

**Parameters:**
- `stock`: yf.Ticker object

**Returns:** Dict with score, reasons, and indicators

##### `get_stock_recommendation(ticker: str)`
Get comprehensive stock recommendation.

**Parameters:**
- `ticker`: Stock symbol

**Returns:** Dict with analysis results

### NewsAnalyzer Class

#### Methods

##### `get_stock_news(ticker: str, days: int = 7)`
Fetch news articles for a specific stock.

**Parameters:**
- `ticker`: Stock symbol
- `days`: Number of days to look back

**Returns:** List of news articles with sentiment

##### `get_market_news(days: int = 7)`
Fetch general market news.

**Parameters:**
- `days`: Number of days to look back

**Returns:** List of market news articles

##### `calculate_news_sentiment_score(articles: List[Dict])`
Calculate overall sentiment score from articles.

**Parameters:**
- `articles`: List of news articles

**Returns:** Dict with sentiment analysis results

### AIAdvisor Class

#### Methods

##### `get_stock_analysis(stock_data: Dict, news_data: List[Dict])`
Generate AI-powered stock analysis.

**Parameters:**
- `stock_data`: Stock analysis results
- `news_data`: News articles for the stock

**Returns:** Dict with AI analysis

##### `get_portfolio_recommendations(portfolio_data: List[Dict])`
Generate portfolio-level recommendations.

**Parameters:**
- `portfolio_data`: List of portfolio stocks

**Returns:** Dict with portfolio analysis

##### `get_market_insights(market_news: List[Dict])`
Generate market insights from news.

**Parameters:**
- `market_news`: List of market news articles

**Returns:** Dict with market insights

## 🔍 Troubleshooting

### Common Issues

#### 1. Missing Dependencies
**Error:** `ModuleNotFoundError: No module named 'streamlit'`

**Solution:**
```bash
pip install -r requirements.txt
```

#### 2. API Key Issues
**Error:** "OpenAI API key not found"

**Solution:**
1. Get API key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. Add to `.env` file:
```env
OPENAI_API_KEY=your_key_here
```

#### 3. Stock Data Not Found
**Error:** "Unable to fetch stock data"

**Solution:**
- Check internet connection
- Verify stock ticker is correct
- Try different stock symbols

#### 4. News API Issues
**Error:** "Error fetching news"

**Solution:**
1. Get API key from [News API](https://newsapi.org/register)
2. Add to `.env` file:
```env
NEWS_API_KEY=your_key_here
```

### Performance Tips

1. **Use API keys** for full functionality
2. **Limit concurrent requests** to avoid rate limits
3. **Cache results** for frequently accessed data
4. **Monitor API usage** to stay within limits

### Debug Mode

Enable debug mode for detailed logging:

```env
DEBUG=True
LOG_LEVEL=DEBUG
```

## ⚠️ Disclaimer

**IMPORTANT:** This application is for **educational and informational purposes only**. It should not be considered as financial advice.

### Key Disclaimers:

1. **Not Financial Advice**: The analysis and recommendations provided are for educational purposes only.

2. **Do Your Own Research**: Always conduct your own research before making investment decisions.

3. **Risk of Loss**: All investments carry risk of loss. Past performance does not guarantee future results.

4. **AI Limitations**: AI analysis may contain errors or inaccuracies.

5. **Market Volatility**: Stock markets are volatile and unpredictable.

6. **Consult Professionals**: Consider consulting with a financial advisor before making investment decisions.

### Educational Use Only

This app is designed to:
- Teach investment concepts
- Demonstrate analysis techniques
- Provide educational insights
- Help understand market dynamics

**It is NOT designed to:**
- Provide financial advice
- Guarantee investment returns
- Replace professional advice
- Make investment decisions for you

## 📞 Support

For support and questions:

1. **Check the documentation** for common issues
2. **Review the troubleshooting section**
3. **Check the GitHub issues** for known problems
4. **Create a new issue** for bugs or feature requests

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Remember:** Always do your own research and consult with financial professionals before making investment decisions. This app is for educational purposes only. 