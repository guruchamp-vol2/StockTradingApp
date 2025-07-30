import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
from typing import Dict, List

# Import our modules
from utils.stock_analyzer import StockAnalyzer
from utils.news_analyzer import NewsAnalyzer
from utils.ai_advisor import AIAdvisor
from config import Config

# Page configuration
st.set_page_config(
    page_title="AI Stock Analyzer & Advisor",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize components
@st.cache_resource
def initialize_components():
    """Initialize analysis components"""
    return StockAnalyzer(), NewsAnalyzer(), AIAdvisor()

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .recommendation-buy {
        color: #28a745;
        font-weight: bold;
    }
    .recommendation-sell {
        color: #dc3545;
        font-weight: bold;
    }
    .recommendation-hold {
        color: #ffc107;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function"""
    
    # Header
    st.markdown('<h1 class="main-header">🤖 AI Stock Analyzer & Advisor</h1>', unsafe_allow_html=True)
    st.markdown("### *Powered by The Motley Fool's Investment Philosophy*")
    
    # Initialize components
    stock_analyzer, news_analyzer, ai_advisor = initialize_components()
    
    # Sidebar
    st.sidebar.title("📊 Navigation")
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["🏠 Dashboard", "🎯 Autonomous Analysis", "🔍 Stock Analysis", "📰 Market News", "📈 Stock Screener", "💼 Portfolio Tracker"]
    )
    
    # API Key Setup
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔑 API Configuration")
    
    openai_key = st.sidebar.text_input("OpenAI API Key", type="password", help="For AI-powered insights")
    news_api_key = st.sidebar.text_input("News API Key", type="password", help="For real-time news")
    
    if openai_key:
        st.session_state['openai_key'] = openai_key
    if news_api_key:
        st.session_state['news_api_key'] = news_api_key
    
    # Main content based on page selection
    if page == "🏠 Dashboard":
        show_dashboard(stock_analyzer, news_analyzer, ai_advisor)
    elif page == "🔍 Stock Analysis":
        show_stock_analysis(stock_analyzer, news_analyzer, ai_advisor)
    elif page == "📰 Market News":
        show_market_news(news_analyzer, ai_advisor)
    elif page == "📈 Stock Screener":
        show_stock_screener(stock_analyzer)
    elif page == "💼 Portfolio Tracker":
        show_portfolio_tracker(stock_analyzer, ai_advisor)
    elif page == "🎯 Autonomous Analysis":
        show_autonomous_analysis(stock_analyzer, news_analyzer, ai_advisor)

def show_dashboard(stock_analyzer, news_analyzer, ai_advisor):
    """Show main dashboard"""
    st.header("📊 Market Dashboard")
    
    # Market overview
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
    
    with st.spinner("Analyzing top stocks..."):
        # Sample top stocks
        top_stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
        recommendations = []
        
        for ticker in top_stocks:
            try:
                result = stock_analyzer.get_stock_recommendation(ticker)
                if result and not result.get('error'):
                    recommendations.append(result)
            except Exception as e:
                st.error(f"Error analyzing {ticker}: {e}")
        
        if recommendations:
            # Create DataFrame for display
            df = pd.DataFrame(recommendations)
            df = df[['ticker', 'current_price', 'overall_score', 'recommendation', 'fundamental_score', 'technical_score']]
            
            # Display recommendations
            for _, row in df.iterrows():
                col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 2])
                
                with col1:
                    st.write(f"**{row['ticker']}**")
                    st.write(f"${row['current_price']:,.2f}")
                
                with col2:
                    st.write("**Score**")
                    st.write(f"{row['overall_score']}/100")
                
                with col3:
                    st.write("**Recommendation**")
                    rec_class = "recommendation-buy" if "BUY" in row['recommendation'] else "recommendation-hold"
                    st.markdown(f'<span class="{rec_class}">{row["recommendation"]}</span>', unsafe_allow_html=True)
                
                with col4:
                    st.write("**Fundamental**")
                    st.write(f"{row['fundamental_score']}/100")
                
                with col5:
                    st.write("**Technical**")
                    st.write(f"{row['technical_score']}/100")
                
                st.markdown("---")
    
    # Market news
    st.subheader("📰 Latest Market News")
    
    with st.spinner("Fetching market news..."):
        market_news = news_analyzer.get_market_news(days=3)
        
        if market_news:
            for article in market_news[:5]:
                with st.expander(f"📰 {article['title']}"):
                    st.write(f"**Source:** {article['source']}")
                    st.write(f"**Published:** {article['published_at'][:10]}")
                    st.write(f"**Sentiment:** {article['sentiment']['sentiment'].title()}")
                    st.write(f"**Summary:** {article['description']}")
                    if article['url'] != '#':
                        st.write(f"[Read More]({article['url']})")

def show_stock_analysis(stock_analyzer, news_analyzer, ai_advisor):
    """Show detailed stock analysis"""
    st.header("🔍 Stock Analysis")
    
    # Stock input
    col1, col2 = st.columns([3, 1])
    
    with col1:
        ticker = st.text_input("Enter Stock Ticker:", placeholder="e.g., AAPL, MSFT, GOOGL").upper()
    
    with col2:
        analyze_button = st.button("🔍 Analyze Stock", type="primary")
    
    if analyze_button and ticker:
        with st.spinner(f"Analyzing {ticker}..."):
            # Get stock analysis
            stock_result = stock_analyzer.get_stock_recommendation(ticker)
            
            if stock_result.get('error'):
                st.error(f"Error analyzing {ticker}: {stock_result['error']}")
                return
            
            # Display results
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                st.metric("Current Price", f"${stock_result['current_price']:,.2f}")
                st.metric("Market Cap", f"${stock_result['market_cap']:,.0f}")
            
            with col2:
                st.metric("Overall Score", f"{stock_result['overall_score']}/100")
                rec_class = "recommendation-buy" if "BUY" in stock_result['recommendation'] else "recommendation-hold"
                st.markdown(f'<span class="{rec_class}">Recommendation: {stock_result["recommendation"]}</span>', unsafe_allow_html=True)
            
            with col3:
                st.metric("Fundamental Score", f"{stock_result['fundamental_score']}/100")
                st.metric("Technical Score", f"{stock_result['technical_score']}/100")
            
            # Detailed analysis tabs
            tab1, tab2, tab3, tab4 = st.tabs(["📊 Analysis", "📈 Technical", "📰 News", "🤖 AI Insights"])
            
            with tab1:
                st.subheader("Fundamental Analysis")
                
                metrics = stock_result['fundamental_metrics']
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Key Metrics:**")
                    st.write(f"P/E Ratio: {metrics.get('pe_ratio', 'N/A')}")
                    st.write(f"P/B Ratio: {metrics.get('pb_ratio', 'N/A')}")
                    st.write(f"ROE: {metrics.get('roe', 'N/A'):.2%}" if metrics.get('roe') else "ROE: N/A")
                    st.write(f"Debt/Equity: {metrics.get('debt_to_equity', 'N/A')}")
                
                with col2:
                    st.write("**Growth Metrics:**")
                    st.write(f"Revenue Growth: {metrics.get('revenue_growth', 'N/A'):.2%}" if metrics.get('revenue_growth') else "Revenue Growth: N/A")
                    st.write(f"Profit Margins: {metrics.get('profit_margins', 'N/A'):.2%}" if metrics.get('profit_margins') else "Profit Margins: N/A")
                    st.write(f"Beta: {metrics.get('beta', 'N/A')}")
                
                st.write("**Strengths:**")
                for reason in stock_result['fundamental_reasons']:
                    st.write(f"✅ {reason}")
            
            with tab2:
                st.subheader("Technical Analysis")
                
                indicators = stock_result['technical_indicators']
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Technical Indicators:**")
                    st.write(f"RSI: {indicators.get('rsi', 'N/A'):.2f}")
                    st.write(f"Price vs MA20: {indicators.get('price_vs_ma20', 'N/A'):.2f}%")
                    st.write(f"Price vs MA50: {indicators.get('price_vs_ma50', 'N/A'):.2f}%")
                    st.write(f"Volume Ratio: {indicators.get('volume_ratio', 'N/A'):.2f}x")
                
                with col2:
                    st.write("**Trend Analysis:**")
                    st.write(f"MACD: {indicators.get('macd', 'N/A'):.4f}")
                    st.write(f"MACD Signal: {indicators.get('macd_signal', 'N/A'):.4f}")
                    st.write(f"BB Position: {indicators.get('bb_position', 'N/A'):.2f}")
                
                st.write("**Technical Signals:**")
                for reason in stock_result['technical_reasons']:
                    st.write(f"📈 {reason}")
            
            with tab3:
                st.subheader("Recent News & Sentiment")
                
                # Get news for the stock
                news_articles = news_analyzer.get_stock_news(ticker, days=7)
                sentiment_score = news_analyzer.calculate_news_sentiment_score(news_articles)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("News Sentiment Score", f"{sentiment_score['score']}/100")
                    st.metric("Articles Analyzed", sentiment_score['article_count'])
                
                with col2:
                    st.metric("Positive Articles", sentiment_score['positive_count'])
                    st.metric("Negative Articles", sentiment_score['negative_count'])
                
                # Display recent articles
                st.write("**Recent Articles:**")
                for article in news_articles[:5]:
                    with st.expander(f"📰 {article['title']}"):
                        st.write(f"**Source:** {article['source']}")
                        st.write(f"**Sentiment:** {article['sentiment']['sentiment'].title()}")
                        st.write(f"**Summary:** {article['description']}")
                        if article['url'] != '#':
                            st.write(f"[Read More]({article['url']})")
            
            with tab4:
                st.subheader("AI-Powered Insights")
                
                # Get AI analysis
                ai_analysis = ai_advisor.get_stock_analysis(stock_result, news_articles)
                
                st.write("**AI Analysis:**")
                st.write(ai_analysis['ai_analysis'])
                
                st.write("**Analysis Details:**")
                st.write(f"- **Ticker:** {ai_analysis['ticker']}")
                st.write(f"- **Score:** {ai_analysis['overall_score']}/100")
                st.write(f"- **Recommendation:** {ai_analysis['recommendation']}")
                st.write(f"- **Analysis Time:** {ai_analysis['timestamp'][:19]}")

def show_market_news(news_analyzer, ai_advisor):
    """Show market news and insights"""
    st.header("📰 Market News & Insights")
    
    # Get market news
    with st.spinner("Fetching market news..."):
        market_news = news_analyzer.get_market_news(days=7)
        sentiment_score = news_analyzer.calculate_news_sentiment_score(market_news)
        
        # Market sentiment overview
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Market Sentiment", f"{sentiment_score['score']}/100")
        
        with col2:
            st.metric("Articles Analyzed", sentiment_score['article_count'])
        
        with col3:
            st.metric("Overall Sentiment", sentiment_score['sentiment'].title())
        
        # AI Market Insights
        st.subheader("🤖 AI Market Insights")
        
        ai_insights = ai_advisor.get_market_insights(market_news)
        st.write(ai_insights['insights'])
        
        # News articles
        st.subheader("📰 Recent Market News")
        
        for article in market_news:
            with st.expander(f"📰 {article['title']}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**Source:** {article['source']}")
                    st.write(f"**Published:** {article['published_at'][:19]}")
                    st.write(f"**Summary:** {article['description']}")
                
                with col2:
                    sentiment = article['sentiment']['sentiment']
                    sentiment_color = "green" if sentiment == "positive" else "red" if sentiment == "negative" else "orange"
                    st.markdown(f"**Sentiment:** :{sentiment_color}[{sentiment.title()}]")
                
                if article['url'] != '#':
                    st.write(f"[Read Full Article]({article['url']})")

def show_stock_screener(stock_analyzer):
    """Show stock screener"""
    st.header("📈 Stock Screener")
    
    # Show database info
    total_stocks = stock_analyzer.get_stock_count()
    st.info(f"📊 Screening {total_stocks} US stocks from NASDAQ, NYSE, and other exchanges")
    
    # Screening criteria
    st.subheader("🔍 Screening Criteria")
    
    col1, col2 = st.columns(2)
    
    with col1:
        min_score = st.slider("Minimum Score", 0, 100, 60)
        min_market_cap = st.number_input("Minimum Market Cap ($B)", 0, 1000, 1)
        max_results = st.number_input("Maximum Results", 10, 500, 100)
    
    with col2:
        max_score = st.slider("Maximum Score", 0, 100, 100, value=100)
        recommendation_filter = st.selectbox("Recommendation Filter", ["All", "STRONG_BUY", "BUY", "HOLD", "SELL", "STRONG_SELL"])
        exchange_filter = st.selectbox("Exchange Filter", ["All", "NASDAQ", "NYSE"])
    
    # Advanced filters
    with st.expander("🔧 Advanced Filters"):
        col1, col2 = st.columns(2)
        
        with col1:
            min_pe_ratio = st.number_input("Min P/E Ratio", 0.0, 100.0, 0.0)
            max_pe_ratio = st.number_input("Max P/E Ratio", 0.0, 100.0, 50.0)
        
        with col2:
            min_roe = st.number_input("Min ROE (%)", 0.0, 100.0, 0.0)
            max_roe = st.number_input("Max ROE (%)", 0.0, 100.0, 100.0)
    
    # Run screener
    if st.button("🔍 Run Comprehensive Screener", type="primary"):
        with st.spinner(f"Screening {total_stocks} stocks... This may take a few minutes."):
            
            # Prepare criteria
            criteria = {
                'min_score': min_score,
                'max_score': max_score,
                'min_market_cap': min_market_cap * 1000000000,  # Convert to actual value
                'max_results': max_results,
                'recommendation': recommendation_filter if recommendation_filter != "All" else None,
                'exchange': exchange_filter if exchange_filter != "All" else None,
                'min_pe_ratio': min_pe_ratio,
                'max_pe_ratio': max_pe_ratio,
                'min_roe': min_roe / 100,  # Convert to decimal
                'max_roe': max_roe / 100
            }
            
            # Run the screener
            results = stock_analyzer.screen_stocks(criteria)
            
            if results:
                st.subheader(f"📊 Found {len(results)} Stocks")
                
                # Create DataFrame
                df = pd.DataFrame(results)
                
                # Select columns to display
                display_columns = ['ticker', 'current_price', 'overall_score', 'recommendation', 
                                 'fundamental_score', 'technical_score', 'market_cap', 'exchange']
                
                # Filter columns that exist
                available_columns = [col for col in display_columns if col in df.columns]
                df_display = df[available_columns]
                
                # Format market cap
                if 'market_cap' in df_display.columns:
                    df_display['market_cap_b'] = df_display['market_cap'] / 1000000000
                    df_display = df_display.drop('market_cap', axis=1)
                    df_display = df_display.rename(columns={'market_cap_b': 'Market Cap ($B)'})
                
                # Display results
                st.dataframe(df_display, use_container_width=True)
                
                # Download option
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Full Results",
                    data=csv,
                    file_name=f"stock_screener_results_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv"
                )
                
                # Show top recommendations
                if len(results) > 0:
                    st.subheader("🏆 Top Recommendations")
                    
                    top_results = results[:5]
                    for i, result in enumerate(top_results, 1):
                        col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
                        
                        with col1:
                            st.write(f"**{i}. {result['ticker']}**")
                            st.write(f"${result['current_price']:,.2f}")
                        
                        with col2:
                            st.write("**Score**")
                            st.write(f"{result['overall_score']}/100")
                        
                        with col3:
                            st.write("**Recommendation**")
                            rec_class = "recommendation-buy" if "BUY" in result['recommendation'] else "recommendation-hold"
                            st.markdown(f'<span class="{rec_class}">{result["recommendation"]}</span>', unsafe_allow_html=True)
                        
                        with col4:
                            st.write("**Exchange**")
                            st.write(result.get('exchange', 'UNKNOWN'))
                        
                        st.markdown("---")
                
                st.success(f"✅ Screening complete! Found {len(results)} stocks matching your criteria.")
            else:
                st.warning("No stocks found matching your criteria. Try relaxing your filters.")
    
    # Quick search
    st.subheader("🔍 Quick Stock Search")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_query = st.text_input("Search by ticker:", placeholder="e.g., AAPL, MSFT, GOOGL")
    
    with col2:
        search_button = st.button("🔍 Search")
    
    if search_button and search_query:
        with st.spinner("Searching stocks..."):
            search_results = stock_analyzer.search_stocks(search_query, limit=20)
            
            if search_results:
                st.write(f"Found {len(search_results)} stocks matching '{search_query}':")
                
                for stock in search_results:
                    st.write(f"- {stock['ticker']} ({stock.get('exchange', 'UNKNOWN')})")
            else:
                st.warning(f"No stocks found matching '{search_query}'")

def show_portfolio_tracker(stock_analyzer, ai_advisor):
    """Show portfolio tracker"""
    st.header("💼 Portfolio Tracker")
    
    # Initialize portfolio in session state
    if 'portfolio' not in st.session_state:
        st.session_state.portfolio = []
    
    # Add stock to portfolio
    st.subheader("➕ Add Stock to Portfolio")
    
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        new_ticker = st.text_input("Ticker:", placeholder="AAPL").upper()
    
    with col2:
        shares = st.number_input("Shares:", min_value=0.0, value=100.0, step=1.0)
    
    with col3:
        if st.button("Add Stock"):
            if new_ticker and shares > 0:
                # Get stock data
                result = stock_analyzer.get_stock_recommendation(new_ticker)
                if result and not result.get('error'):
                    portfolio_item = {
                        'ticker': new_ticker,
                        'shares': shares,
                        'current_price': result['current_price'],
                        'overall_score': result['overall_score'],
                        'recommendation': result['recommendation'],
                        'fundamental_score': result['fundamental_score'],
                        'technical_score': result['technical_score']
                    }
                    st.session_state.portfolio.append(portfolio_item)
                    st.success(f"Added {new_ticker} to portfolio!")
                else:
                    st.error(f"Could not fetch data for {new_ticker}")
    
    # Display portfolio
    if st.session_state.portfolio:
        st.subheader("📊 Your Portfolio")
        
        # Calculate portfolio metrics
        total_value = sum(item['current_price'] * item['shares'] for item in st.session_state.portfolio)
        avg_score = sum(item['overall_score'] for item in st.session_state.portfolio) / len(st.session_state.portfolio)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Value", f"${total_value:,.2f}")
        
        with col2:
            st.metric("Average Score", f"{avg_score:.1f}/100")
        
        with col3:
            st.metric("Number of Stocks", len(st.session_state.portfolio))
        
        # Portfolio table
        portfolio_df = pd.DataFrame(st.session_state.portfolio)
        portfolio_df['value'] = portfolio_df['current_price'] * portfolio_df['shares']
        portfolio_df['weight'] = portfolio_df['value'] / total_value * 100
        
        st.dataframe(portfolio_df, use_container_width=True)
        
        # AI Portfolio Analysis
        st.subheader("🤖 AI Portfolio Analysis")
        
        ai_portfolio = ai_advisor.get_portfolio_recommendations(st.session_state.portfolio)
        st.write(ai_portfolio['analysis'])
        
        # Remove stocks
        st.subheader("🗑️ Remove Stocks")
        
        if st.session_state.portfolio:
            ticker_to_remove = st.selectbox("Select stock to remove:", [item['ticker'] for item in st.session_state.portfolio])
            
            if st.button("Remove Stock"):
                st.session_state.portfolio = [item for item in st.session_state.portfolio if item['ticker'] != ticker_to_remove]
                st.success(f"Removed {ticker_to_remove} from portfolio!")
                st.rerun()
    else:
        st.info("Your portfolio is empty. Add some stocks to get started!")

def show_autonomous_analysis(stock_analyzer, news_analyzer, ai_advisor):
    """Show autonomous stock analysis with complete recommendations"""
    st.header("🎯 Autonomous Stock Analysis")
    st.info("Get complete, actionable investment recommendations that require NO additional research!")
    
    # User profile section
    st.subheader("👤 Your Investment Profile")
    st.write("This helps us provide personalized recommendations.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        risk_tolerance = st.selectbox(
            "Risk Tolerance:",
            ["conservative", "moderate", "aggressive"],
            help="Conservative: Lower risk, lower returns. Aggressive: Higher risk, higher potential returns."
        )
        
        investment_horizon = st.selectbox(
            "Investment Horizon:",
            ["short_term", "medium_term", "long_term"],
            help="Short term: 1-12 months. Medium term: 1-3 years. Long term: 3+ years."
        )
    
    with col2:
        investment_amount = st.number_input(
            "Investment Amount ($):",
            min_value=1000,
            max_value=1000000,
            value=10000,
            step=1000
        )
        
        experience_level = st.selectbox(
            "Experience Level:",
            ["beginner", "intermediate", "advanced"],
            help="Beginner: New to investing. Advanced: Experienced investor."
        )
    
    # Stock input
    st.subheader("📊 Stock Analysis")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        ticker = st.text_input("Enter Stock Ticker:", placeholder="AAPL, MSFT, GOOGL").upper()
    
    with col2:
        analyze_button = st.button("🎯 Get Autonomous Recommendation", type="primary")
    
    if analyze_button and ticker:
        with st.spinner(f"Generating complete analysis for {ticker}..."):
            # Get stock data
            stock_result = stock_analyzer.get_stock_recommendation(ticker)
            
            if stock_result.get('error'):
                st.error(f"Error analyzing {ticker}: {stock_result['error']}")
                return
            
            # Get news data
            news_data = news_analyzer.get_stock_news(ticker)
            
            # Create user profile
            user_profile = {
                'risk_tolerance': risk_tolerance,
                'investment_horizon': investment_horizon,
                'investment_amount': investment_amount,
                'experience_level': experience_level
            }
            
            # Get autonomous recommendation
            autonomous_rec = ai_advisor.get_autonomous_recommendation(stock_result, news_data, user_profile)
            
            # Display results
            st.success("✅ Complete analysis ready! You can implement this recommendation immediately.")
            
            # Key metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Current Price", f"${stock_result['current_price']:,.2f}")
            
            with col2:
                confidence = autonomous_rec.get('confidence_score', 0)
                st.metric("Confidence", f"{confidence:.1%}")
            
            with col3:
                risk_level = autonomous_rec.get('risk_assessment', {}).get('risk_level', 'Unknown')
                st.metric("Risk Level", risk_level)
            
            with col4:
                position_size = autonomous_rec.get('position_sizing', {}).get('percentage', 0)
                st.metric("Position Size", f"{position_size:.1f}%")
            
            # Main recommendation
            st.subheader("🎯 COMPLETE INVESTMENT RECOMMENDATION")
            st.markdown(autonomous_rec.get('recommendation', ''))
            
            # Detailed breakdown
            tab1, tab2, tab3, tab4 = st.tabs(["💰 Entry/Exit Strategy", "📊 Risk Analysis", "📈 Technical Details", "📰 News Impact"])
            
            with tab1:
                st.write("**Entry Strategy:**")
                entry_strategy = autonomous_rec.get('entry_strategy', {})
                st.write(f"• Immediate Entry: ${entry_strategy.get('immediate_entry', 0):,.2f}")
                st.write(f"• Dollar Cost Average: ${entry_strategy.get('dollar_cost_average', 0):,.2f}")
                st.write(f"• Entry Timing: {entry_strategy.get('entry_timing', 'N/A')}")
                
                st.write("**Exit Strategy:**")
                exit_strategy = autonomous_rec.get('exit_strategy', {})
                st.write(f"• Stop Loss: ${exit_strategy.get('stop_loss', 0):,.2f}")
                st.write(f"• Profit Targets:")
                for i, target in enumerate(exit_strategy.get('profit_targets', []), 1):
                    st.write(f"  - Target {i}: ${target:,.2f}")
                
                st.write("**Position Sizing:**")
                position_sizing = autonomous_rec.get('position_sizing', {})
                st.write(f"• Recommended Amount: ${position_sizing.get('dollar_amount', 0):,.2f}")
                st.write(f"• Number of Shares: {position_sizing.get('shares', 0)}")
                st.write(f"• Max Position: {position_sizing.get('max_position', 0):.1f}%")
            
            with tab2:
                risk_assessment = autonomous_rec.get('risk_assessment', {})
                
                st.write("**Risk Assessment:**")
                st.write(f"• Risk Level: {risk_assessment.get('risk_level', 'Unknown')}")
                st.write(f"• Beta: {risk_assessment.get('beta', 'N/A')}")
                st.write(f"• Volatility: {risk_assessment.get('volatility', 'Unknown')}")
                st.write(f"• Score Risk: {risk_assessment.get('score_risk', 'Unknown')}")
                
                st.write("**Risk Management:**")
                st.write("• Set stop-loss orders immediately")
                st.write("• Don't invest more than you can afford to lose")
                st.write("• Diversify across different sectors")
                st.write("• Monitor positions regularly")
            
            with tab3:
                if stock_result.get('technical_indicators'):
                    indicators = stock_result['technical_indicators']
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Technical Indicators:**")
                        st.write(f"RSI: {indicators.get('rsi', 'N/A'):.2f}")
                        st.write(f"MACD: {indicators.get('macd', 'N/A'):.4f}")
                        st.write(f"BB Position: {indicators.get('bb_position', 'N/A'):.2f}")
                    
                    with col2:
                        st.write("**Moving Averages:**")
                        st.write(f"MA20: ${indicators.get('ma_20', 'N/A'):,.2f}")
                        st.write(f"MA50: ${indicators.get('ma_50', 'N/A'):,.2f}")
                        st.write(f"Price vs MA20: {indicators.get('price_vs_ma20', 'N/A'):.2f}%")
                    
                    st.write("**Technical Signals:**")
                    for reason in stock_result.get('technical_reasons', []):
                        st.write(f"📈 {reason}")
                else:
                    st.info("Technical indicators not available.")
            
            with tab4:
                if news_data:
                    sentiment_scores = [article.get('sentiment', {}).get('polarity', 0) for article in news_data]
                    avg_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("News Sentiment", f"{avg_sentiment:.2f}")
                    
                    with col2:
                        st.metric("News Count", len(news_data))
                    
                    st.write("**Recent News Impact:**")
                    for i, article in enumerate(news_data[:3]):
                        with st.expander(f"📰 {article.get('title', 'No title')}"):
                            st.write(f"**Sentiment:** {article.get('sentiment', {}).get('sentiment', 'Neutral')}")
                            st.write(f"**Summary:** {article.get('description', 'No description')}")
                else:
                    st.info("No recent news available for this stock.")
            
            # Monitoring points
            st.subheader("📊 Monitoring Points")
            monitoring_points = autonomous_rec.get('monitoring_points', [])
            
            for point in monitoring_points:
                st.write(f"• **{point.get('metric', 'Unknown')}**: {point.get('frequency', 'Unknown')} - {point.get('alert_levels', 'N/A')}")
            
            # Implementation checklist
            st.subheader("✅ Implementation Checklist")
            st.write("Follow these steps to implement your investment:")
            st.write("1. ✅ Review the recommendation above")
            st.write("2. ✅ Set your entry price and stop loss")
            st.write("3. ✅ Calculate your position size")
            st.write("4. ✅ Place your order through your broker")
            st.write("5. ✅ Set up monitoring alerts")
            st.write("6. ✅ Review your position weekly")
            
            # Disclaimer
            st.warning("⚠️ **Disclaimer**: This analysis is for educational purposes only. Always do your own research and consider consulting a financial advisor before making investment decisions.")

if __name__ == "__main__":
    main() 