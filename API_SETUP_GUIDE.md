# 🔑 API Keys Setup Guide

This guide will help you set up the API keys needed for the AI Stock Analyzer app to work optimally.

## 📋 Required API Keys

### 1. **OpenAI API Key** (Recommended)
- **Purpose**: AI-powered stock analysis and recommendations
- **Get it from**: [OpenAI Platform](https://platform.openai.com/api-keys)
- **Cost**: Pay-per-use (very affordable for personal use)
- **Required for**: Autonomous analysis, AI insights, comprehensive recommendations

### 2. **News API Key** (Recommended)
- **Purpose**: Real-time financial news and sentiment analysis
- **Get it from**: [NewsAPI.org](https://newsapi.org/register)
- **Cost**: Free tier available (1000 requests/day)
- **Required for**: News sentiment analysis, market insights

### 3. **Alpha Vantage API Key** (Optional)
- **Purpose**: Additional market data and technical indicators
- **Get it from**: [Alpha Vantage](https://www.alphavantage.co/support/#api-key)
- **Cost**: Free tier available (500 requests/day)
- **Required for**: Enhanced technical analysis

## 🚀 Step-by-Step Setup

### Step 1: Create .env file

Create a file named `.env` in your project root directory:

```bash
# In your StockTradingApp directory
touch .env
```

### Step 2: Add your API keys

Open the `.env` file and add your API keys:

```env
# AI Stock Analyzer - API Keys Configuration

# OpenAI API Key (Required for AI-powered insights)
# Get your key from: https://platform.openai.com/api-keys
OPENAI_API_KEY=your_openai_api_key_here

# News API Key (Required for real-time financial news)
# Get your key from: https://newsapi.org/register
NEWS_API_KEY=your_news_api_key_here

# Alpha Vantage API Key (Optional - for additional market data)
# Get your key from: https://www.alphavantage.co/support/#api-key
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key_here

# Application Settings
DEBUG=True
LOG_LEVEL=INFO
```

### Step 3: Get your API keys

#### **OpenAI API Key:**
1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign up or log in to your account
3. Click "Create new secret key"
4. Copy the generated key
5. Replace `your_openai_api_key_here` in your `.env` file

#### **News API Key:**
1. Go to [NewsAPI.org](https://newsapi.org/register)
2. Sign up for a free account
3. Verify your email
4. Copy your API key from the dashboard
5. Replace `your_news_api_key_here` in your `.env` file

#### **Alpha Vantage API Key (Optional):**
1. Go to [Alpha Vantage](https://www.alphavantage.co/support/#api-key)
2. Sign up for a free account
3. Copy your API key
4. Replace `your_alpha_vantage_api_key_here` in your `.env` file

### Step 4: Verify setup

Run the setup script to verify your API keys:

```bash
python setup.py
```

## 🔒 Security Best Practices

### **Never commit your .env file**
The `.env` file is already in `.gitignore` to prevent accidentally committing your API keys.

### **Keep your keys secure**
- Don't share your API keys publicly
- Don't hardcode them in your source code
- Use environment variables (which the app already does)

### **Monitor API usage**
- OpenAI: Check usage at [OpenAI Platform](https://platform.openai.com/usage)
- News API: Check usage in your [NewsAPI dashboard](https://newsapi.org/account)
- Alpha Vantage: Check usage in your [Alpha Vantage dashboard](https://www.alphavantage.co/support/#api-key)

## 💰 Cost Estimates

### **Free Tier Usage (Recommended for beginners):**
- **OpenAI**: ~$0.01-0.10 per day for personal use
- **News API**: 1000 requests/day (free)
- **Alpha Vantage**: 500 requests/day (free)

### **Typical Monthly Cost:**
- **Light usage**: $1-5/month
- **Heavy usage**: $10-20/month
- **Professional usage**: $50+/month

## 🎯 What Each API Enables

### **With OpenAI API:**
✅ Complete autonomous investment recommendations  
✅ AI-powered stock analysis  
✅ Personalized portfolio advice  
✅ Market insights and trends  
✅ Risk assessment and management  

### **With News API:**
✅ Real-time financial news  
✅ News sentiment analysis  
✅ Market impact assessment  
✅ Sector-specific news filtering  

### **With Alpha Vantage:**
✅ Enhanced technical indicators  
✅ Real-time market data  
✅ Historical price analysis  
✅ Advanced charting capabilities  

## 🚨 Troubleshooting

### **"API key not found" error:**
1. Check that your `.env` file exists in the project root
2. Verify the API key variable names match exactly
3. Restart the application after adding keys

### **"Rate limit exceeded" error:**
1. Check your API usage in the respective dashboards
2. Consider upgrading to a paid plan
3. Implement request caching (already built into the app)

### **"Invalid API key" error:**
1. Verify you copied the key correctly
2. Check that the key is active in your account
3. Ensure you're using the correct API endpoint

## 🎉 Next Steps

Once you've set up your API keys:

1. **Run the app**: `python run.py`
2. **Test the features**: Try the autonomous analysis
3. **Monitor usage**: Check your API dashboards regularly
4. **Enjoy**: Get complete investment recommendations!

## 📞 Need Help?

If you encounter any issues:
1. Check the troubleshooting section above
2. Review the API documentation links
3. Check your API usage limits
4. Ensure your `.env` file is properly formatted

---

**⚠️ Important**: Never share your API keys publicly. The app is designed to keep them secure using environment variables. 