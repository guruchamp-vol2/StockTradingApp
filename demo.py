#!/usr/bin/env python3
"""
Demo script for AI Stock Analyzer & Advisor
Shows the app's capabilities with sample data
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np

def run_demo():
    """Run the demo application"""
    
    st.set_page_config(
        page_title="AI Stock Analyzer Demo",
        page_icon="📈",
        layout="wide"
    )
    
    st.markdown("""
    <style>
        .demo-header {
            font-size: 2.5rem;
            font-weight: bold;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 2rem;
        }
        .feature-card {
            background-color: #f0f2f6;
            padding: 1.5rem;
            border-radius: 0.5rem;
            border-left: 4px solid #1f77b4;
            margin: 1rem 0;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="demo-header">🤖 AI Stock Analyzer Demo</h1>', unsafe_allow_html=True)
    st.markdown("### *Experience the power of AI-driven stock analysis*")
    
    # Demo navigation
    st.sidebar.title("📊 Demo Features")
    demo_page = st.sidebar.selectbox(
        "Choose a demo:",
        ["🏠 Overview", "🔍 Stock Analysis", "📰 News Analysis", "📈 Screener", "💼 Portfolio", "🤖 AI Insights"]
    )
    
    if demo_page == "🏠 Overview":
        show_overview_demo()
    elif demo_page == "🔍 Stock Analysis":
        show_stock_analysis_demo()
    elif demo_page == "📰 News Analysis":
        show_news_analysis_demo()
    elif demo_page == "📈 Screener":
        show_screener_demo()
    elif demo_page == "💼 Portfolio":
        show_portfolio_demo()
    elif demo_page == "🤖 AI Insights":
        show_ai_insights_demo()

def show_overview_demo():
    """Show overview demo"""
    st.header("🏠 App Overview")
    
    st.markdown("""
    <div class="feature-card">
        <h3>🎯 Smart Stock Recommendations</h3>
        <p>Our AI analyzes stocks using The Motley Fool's proven 8-step process:</p>
        <ul>
            <li>✅ Understand the business model</li>
            <li>✅ Look for competitive advantages</li>
            <li>✅ Dig into the numbers</li>
            <li>✅ Prove yourself wrong</li>
            <li>✅ Learn to say "no"</li>
            <li>✅ Learn from mistakes</li>
            <li>✅ Learn from successes</li>
            <li>✅ Invest in knowledge</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Sample market data
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("S&P 500", "4,185.48", "+0.85%")
    with col2:
        st.metric("NASDAQ", "12,888.95", "+1.23%")
    with col3:
        st.metric("DOW", "33,886.47", "+0.45%")
    with col4:
        st.metric("VIX", "18.25", "-2.1%")
    
    # Top recommendations
    st.subheader("🎯 Top Stock Recommendations")
    
    sample_recommendations = [
        {"ticker": "AAPL", "score": 85, "recommendation": "STRONG_BUY", "price": 175.43},
        {"ticker": "MSFT", "score": 82, "recommendation": "STRONG_BUY", "price": 338.11},
        {"ticker": "GOOGL", "score": 78, "recommendation": "BUY", "price": 142.56},
        {"ticker": "AMZN", "score": 75, "recommendation": "BUY", "price": 145.24},
        {"ticker": "TSLA", "score": 68, "recommendation": "BUY", "price": 248.42}
    ]
    
    for rec in sample_recommendations:
        col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
        
        with col1:
            st.write(f"**{rec['ticker']}**")
            st.write(f"${rec['price']:,.2f}")
        
        with col2:
            st.write("**Score**")
            st.write(f"{rec['score']}/100")
        
        with col3:
            st.write("**Recommendation**")
            if "BUY" in rec['recommendation']:
                st.markdown(f'<span style="color: #28a745; font-weight: bold;">{rec["recommendation"]}</span>', unsafe_allow_html=True)
            else:
                st.markdown(f'<span style="color: #ffc107; font-weight: bold;">{rec["recommendation"]}</span>', unsafe_allow_html=True)
        
        with col4:
            st.write("**Analysis**")
            st.write("✅ Strong fundamentals")
        
        st.markdown("---")

def show_stock_analysis_demo():
    """Show stock analysis demo"""
    st.header("🔍 Stock Analysis Demo")
    
    # Sample stock data
    ticker = st.selectbox("Select a stock to analyze:", ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"])
    
    if ticker:
        st.subheader(f"📊 Analysis for {ticker}")
        
        # Sample analysis data
        analysis_data = {
            "AAPL": {"price": 175.43, "score": 85, "fundamental": 88, "technical": 82, "recommendation": "STRONG_BUY"},
            "MSFT": {"price": 338.11, "score": 82, "fundamental": 85, "technical": 79, "recommendation": "STRONG_BUY"},
            "GOOGL": {"price": 142.56, "score": 78, "fundamental": 80, "technical": 76, "recommendation": "BUY"},
            "AMZN": {"price": 145.24, "score": 75, "fundamental": 78, "technical": 72, "recommendation": "BUY"},
            "TSLA": {"price": 248.42, "score": 68, "fundamental": 70, "technical": 66, "recommendation": "BUY"}
        }
        
        data = analysis_data[ticker]
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Current Price", f"${data['price']:,.2f}")
        with col2:
            st.metric("Overall Score", f"{data['score']}/100")
        with col3:
            st.metric("Fundamental Score", f"{data['fundamental']}/100")
        with col4:
            st.metric("Technical Score", f"{data['technical']}/100")
        
        # Analysis tabs
        tab1, tab2, tab3 = st.tabs(["📊 Analysis", "📈 Technical", "🤖 AI Insights"])
        
        with tab1:
            st.subheader("Fundamental Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Key Metrics:**")
                st.write("P/E Ratio: 25.4")
                st.write("P/B Ratio: 12.8")
                st.write("ROE: 18.5%")
                st.write("Debt/Equity: 0.35")
            
            with col2:
                st.write("**Growth Metrics:**")
                st.write("Revenue Growth: 12.3%")
                st.write("Profit Margins: 24.8%")
                st.write("Beta: 1.15")
            
            st.write("**Strengths:**")
            st.write("✅ Strong competitive advantages")
            st.write("✅ Excellent financial metrics")
            st.write("✅ Consistent revenue growth")
            st.write("✅ Low debt levels")
        
        with tab2:
            st.subheader("Technical Analysis")
            
            # Sample technical indicators
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Technical Indicators:**")
                st.write("RSI: 58.2")
                st.write("Price vs MA20: +2.3%")
                st.write("Price vs MA50: +8.7%")
                st.write("Volume Ratio: 1.2x")
            
            with col2:
                st.write("**Trend Analysis:**")
                st.write("MACD: 0.0234")
                st.write("MACD Signal: 0.0187")
                st.write("BB Position: 0.65")
            
            st.write("**Technical Signals:**")
            st.write("📈 Price above moving averages")
            st.write("📈 Positive MACD crossover")
            st.write("📈 Above average volume")
        
        with tab3:
            st.subheader("AI-Powered Insights")
            
            ai_analysis = f"""
            **Investment Thesis:**
            {ticker} demonstrates strong fundamentals with excellent competitive advantages. 
            The company shows consistent growth and solid financial metrics.
            
            **Key Strengths:**
            - Strong brand recognition and customer loyalty
            - Robust financial position with low debt
            - Consistent revenue and earnings growth
            - Innovative product pipeline
            
            **Risk Factors:**
            - Market volatility and economic uncertainty
            - Regulatory challenges in some markets
            - Competition from emerging players
            
            **Recommendation:**
            Consider {ticker} for long-term growth potential. Monitor for entry opportunities 
            during market pullbacks. Diversify across sectors for risk management.
            """
            
            st.write(ai_analysis)

def show_news_analysis_demo():
    """Show news analysis demo"""
    st.header("📰 News Analysis Demo")
    
    # Sample news data
    sample_news = [
        {
            "title": "Tech Stocks Rally on Strong Earnings Reports",
            "source": "Financial Times",
            "sentiment": "positive",
            "description": "Technology sector sees broad gains following positive earnings reports from major companies."
        },
        {
            "title": "Federal Reserve Maintains Interest Rates",
            "source": "Reuters",
            "sentiment": "neutral",
            "description": "The Fed keeps rates steady, signaling continued economic stability."
        },
        {
            "title": "Oil Prices Decline on Supply Concerns",
            "source": "Market Watch",
            "sentiment": "negative",
            "description": "Crude oil prices fall amid global supply chain issues."
        }
    ]
    
    # Market sentiment
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Market Sentiment", "65/100")
    with col2:
        st.metric("Articles Analyzed", "15")
    with col3:
        st.metric("Overall Sentiment", "Positive")
    
    # News articles
    st.subheader("📰 Recent Market News")
    
    for article in sample_news:
        with st.expander(f"📰 {article['title']}"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**Source:** {article['source']}")
                st.write(f"**Summary:** {article['description']}")
            
            with col2:
                sentiment_color = "green" if article['sentiment'] == "positive" else "red" if article['sentiment'] == "negative" else "orange"
                st.markdown(f"**Sentiment:** :{sentiment_color}[{article['sentiment'].title()}]")
    
    # AI Market Insights
    st.subheader("🤖 AI Market Insights")
    
    insights = """
    **Key Market Trends:**
    - Technology sector leading market gains
    - Defensive positioning in uncertain markets
    - Focus on quality companies with strong fundamentals
    
    **Investment Opportunities:**
    - Consider tech stocks with strong earnings
    - Look for defensive stocks in volatile markets
    - Monitor interest rate decisions for bond investments
    
    **Risk Factors:**
    - Economic uncertainty and inflation concerns
    - Geopolitical tensions affecting supply chains
    - Regulatory changes in key sectors
    """
    
    st.write(insights)

def show_screener_demo():
    """Show screener demo"""
    st.header("📈 Stock Screener Demo")
    
    # Screening criteria
    st.subheader("🔍 Screening Criteria")
    
    col1, col2 = st.columns(2)
    
    with col1:
        min_score = st.slider("Minimum Score", 0, 100, 60)
        min_market_cap = st.number_input("Minimum Market Cap ($B)", 0, 1000, 10)
    
    with col2:
        max_score = st.slider("Maximum Score", 0, 100, 100, value=100)
        recommendation_filter = st.selectbox("Recommendation Filter", ["All", "STRONG_BUY", "BUY", "HOLD"])
    
    if st.button("🔍 Run Screener"):
        st.subheader("📊 Screening Results")
        
        # Sample screener results
        results = [
            {"ticker": "AAPL", "price": 175.43, "score": 85, "recommendation": "STRONG_BUY", "market_cap": 2750},
            {"ticker": "MSFT", "price": 338.11, "score": 82, "recommendation": "STRONG_BUY", "market_cap": 2510},
            {"ticker": "GOOGL", "price": 142.56, "score": 78, "recommendation": "BUY", "market_cap": 1780},
            {"ticker": "AMZN", "price": 145.24, "score": 75, "recommendation": "BUY", "market_cap": 1510},
            {"ticker": "NVDA", "price": 485.09, "score": 72, "recommendation": "BUY", "market_cap": 1190}
        ]
        
        # Filter results based on criteria
        filtered_results = [r for r in results if min_score <= r['score'] <= max_score and r['market_cap'] >= min_market_cap]
        
        if recommendation_filter != "All":
            filtered_results = [r for r in filtered_results if r['recommendation'] == recommendation_filter]
        
        if filtered_results:
            df = pd.DataFrame(filtered_results)
            st.dataframe(df, use_container_width=True)
            
            st.success(f"Found {len(filtered_results)} stocks matching your criteria!")
        else:
            st.warning("No stocks found matching your criteria.")

def show_portfolio_demo():
    """Show portfolio demo"""
    st.header("💼 Portfolio Tracker Demo")
    
    # Sample portfolio
    sample_portfolio = [
        {"ticker": "AAPL", "shares": 100, "price": 175.43, "score": 85, "recommendation": "STRONG_BUY"},
        {"ticker": "MSFT", "shares": 50, "price": 338.11, "score": 82, "recommendation": "STRONG_BUY"},
        {"ticker": "GOOGL", "shares": 75, "price": 142.56, "score": 78, "recommendation": "BUY"},
        {"ticker": "AMZN", "shares": 60, "price": 145.24, "score": 75, "recommendation": "BUY"}
    ]
    
    # Calculate portfolio metrics
    total_value = sum(item['price'] * item['shares'] for item in sample_portfolio)
    avg_score = sum(item['score'] for item in sample_portfolio) / len(sample_portfolio)
    
    # Portfolio overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Value", f"${total_value:,.2f}")
    with col2:
        st.metric("Average Score", f"{avg_score:.1f}/100")
    with col3:
        st.metric("Number of Stocks", len(sample_portfolio))
    
    # Portfolio table
    st.subheader("📊 Your Portfolio")
    
    portfolio_df = pd.DataFrame(sample_portfolio)
    portfolio_df['value'] = portfolio_df['price'] * portfolio_df['shares']
    portfolio_df['weight'] = portfolio_df['value'] / total_value * 100
    
    st.dataframe(portfolio_df, use_container_width=True)
    
    # AI Portfolio Analysis
    st.subheader("🤖 AI Portfolio Analysis")
    
    analysis = """
    **Portfolio Health Assessment:**
    Your portfolio shows good diversification across technology stocks with strong fundamentals.
    The average score of 80/100 indicates solid stock selection.
    
    **Diversification Analysis:**
    - Technology sector concentration: 100%
    - Consider adding defensive stocks
    - Geographic diversification could be improved
    
    **Risk Assessment:**
    - Moderate risk due to sector concentration
    - Strong individual stock fundamentals
    - Consider adding bonds or defensive stocks
    
    **Recommendations:**
    - Add healthcare or consumer staples stocks
    - Consider international exposure
    - Monitor for rebalancing opportunities
    """
    
    st.write(analysis)

def show_ai_insights_demo():
    """Show AI insights demo"""
    st.header("🤖 AI Insights Demo")
    
    st.subheader("🎯 Investment Philosophy")
    
    philosophy = """
    Our AI follows The Motley Fool's proven 8-step investment process:
    
    1. **Understand the Business Model** - Invest in what you know
    2. **Look for Competitive Advantages** - Find companies with moats
    3. **Dig into the Numbers** - Analyze fundamentals thoroughly
    4. **Prove Yourself Wrong** - Challenge your own analysis
    5. **Learn to Say "No"** - Be selective about investments
    6. **Learn from Mistakes** - Review and improve continuously
    7. **Learn from Successes** - Understand what went right
    8. **Invest in Knowledge** - Continuous learning is key
    """
    
    st.write(philosophy)
    
    # AI Analysis Example
    st.subheader("🔍 Sample AI Analysis")
    
    sample_analysis = """
    **Stock: AAPL (Apple Inc.)**
    
    **Investment Thesis:**
    Apple demonstrates exceptional competitive advantages through its ecosystem, brand loyalty, 
    and innovation pipeline. The company's strong financial position and consistent growth 
    make it an attractive long-term investment.
    
    **Key Strengths:**
    - Unmatched brand recognition and customer loyalty
    - Robust ecosystem lock-in effect
    - Strong cash flow and balance sheet
    - Innovation in services and wearables
    
    **Risk Factors:**
    - Dependence on iPhone sales
    - Regulatory scrutiny in app store
    - Supply chain vulnerabilities
    - Market saturation in developed markets
    
    **Entry/Exit Strategy:**
    Consider accumulating on market pullbacks. Set stop-loss at 10% below entry.
    Hold for 3-5 years minimum to capture long-term growth.
    
    **Long-term Outlook:**
    Positive outlook based on services growth, wearables expansion, and ecosystem strength.
    Expect continued innovation and market share gains.
    """
    
    st.write(sample_analysis)
    
    # AI Features
    st.subheader("🚀 AI Features")
    
    features = """
    **Real-time Analysis:**
    - Live stock data and technical indicators
    - Fundamental analysis using multiple metrics
    - News sentiment analysis
    
    **Smart Recommendations:**
    - Multi-factor scoring system (0-100)
    - Personalized recommendations
    - Risk assessment and management
    
    **Portfolio Optimization:**
    - Diversification analysis
    - Risk assessment
    - Rebalancing suggestions
    
    **Market Insights:**
    - Trend analysis
    - Sector rotation opportunities
    - Economic impact assessment
    """
    
    st.write(features)

if __name__ == "__main__":
    run_demo() 