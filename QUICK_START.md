# 🚀 Quick Start Guide

Get the AI Stock Analyzer running in 5 minutes!

## ⚡ Super Quick Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up API Keys (2 minutes)
```bash
python setup_api_keys.py
```
Follow the prompts to add your API keys:
- **OpenAI API Key**: Get from [OpenAI Platform](https://platform.openai.com/api-keys) (free credits available)
- **News API Key**: Get from [NewsAPI.org](https://newsapi.org/register) (free tier available)
- **Alpha Vantage API Key**: Get from [Alpha Vantage](https://www.alphavantage.co/support/#api-key) (optional, free tier available)

### 3. Run the App
```bash
python run.py
```

### 4. Open Your Browser
Go to: `http://localhost:8501`

## 🎯 What You'll Get

✅ **Complete stock analysis** for any US stock  
✅ **Autonomous investment recommendations** with exact prices  
✅ **Real-time news and sentiment analysis**  
✅ **Portfolio tracking and management**  
✅ **Comprehensive stock screening** across 100+ stocks  

## 💰 Cost Estimate

**Free tier usage** (recommended for beginners):
- **OpenAI**: ~$0.01-0.10 per day
- **News API**: 1000 requests/day (free)
- **Alpha Vantage**: 500 requests/day (free)

**Total**: ~$1-5/month for personal use

## 🔑 API Keys Explained

### **OpenAI API Key** (Most Important)
- **Purpose**: AI-powered stock analysis and recommendations
- **Cost**: Pay-per-use (very affordable)
- **Required for**: Autonomous analysis, AI insights, complete recommendations

### **News API Key** (Recommended)
- **Purpose**: Real-time financial news and sentiment analysis
- **Cost**: Free tier available
- **Required for**: News sentiment analysis, market insights

### **Alpha Vantage API Key** (Optional)
- **Purpose**: Additional market data and technical indicators
- **Cost**: Free tier available
- **Required for**: Enhanced technical analysis

## 🎉 Try It Out

1. **Go to "🎯 Autonomous Analysis"** in the app
2. **Set your investment profile** (risk tolerance, amount, etc.)
3. **Enter a stock ticker** (try: AAPL, MSFT, GOOGL)
4. **Get complete recommendation** with exact prices and action plan

## 🆘 Need Help?

- **API Setup Issues**: Check `API_SETUP_GUIDE.md`
- **App Not Starting**: Run `python test_app.py` to check dependencies
- **API Key Errors**: Verify your keys in the respective dashboards

## 🔒 Security

Your API keys are stored securely in a `.env` file that is:
- ✅ **Not committed to Git** (in `.gitignore`)
- ✅ **Local to your machine only**
- ✅ **Protected from accidental sharing**

---

**🎯 Goal**: Get complete, actionable investment recommendations without doing additional research! 