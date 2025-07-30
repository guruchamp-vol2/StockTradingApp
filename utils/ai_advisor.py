import openai
from typing import Dict, List, Optional
import logging
import json
from datetime import datetime

from config import Config
from utils.local_ai_advisor import LocalAIAdvisor
from utils.enhanced_local_ai import EnhancedLocalAI
from utils.free_llm_integration import FreeLLMIntegration

class AIAdvisor:
    """AI-powered stock advisor using OpenAI GPT with comprehensive analysis"""
    
    def __init__(self):
        self.config = Config()
        self.logger = logging.getLogger(__name__)
        
        # Initialize enhanced local AI advisor as fallback
        self.local_advisor = LocalAIAdvisor()
        self.enhanced_advisor = EnhancedLocalAI()
        self.free_llm = FreeLLMIntegration()
        
        if self.config.OPENAI_API_KEY:
            openai.api_key = self.config.OPENAI_API_KEY
            self.use_openai = True
        else:
            self.logger.info("OpenAI API key not found. Using local AI advisor (completely free!).")
            self.use_openai = False
    
    def get_stock_analysis(self, stock_data: Dict, news_data: List[Dict]) -> Dict:
        """Generate comprehensive AI-powered stock analysis"""
        if not self.use_openai:
            return self.free_llm.get_free_analysis(stock_data, news_data)
        
        try:
            # Prepare context for AI
            context = self._prepare_analysis_context(stock_data, news_data)
            
            # Create comprehensive prompt for analysis
            prompt = self._create_comprehensive_analysis_prompt(context)
            
            # Get AI response
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self._get_comprehensive_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            
            # Parse AI response
            analysis = self._parse_comprehensive_ai_response(ai_response, stock_data)
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error in OpenAI analysis: {e}")
            return self.free_llm.get_free_analysis(stock_data, news_data)
    
    def get_autonomous_recommendation(self, stock_data: Dict, news_data: List[Dict], user_profile: Dict = None) -> Dict:
        """Generate autonomous investment recommendation without requiring user research"""
        if not self.use_openai:
            return self.enhanced_advisor.get_autonomous_recommendation(stock_data, news_data, user_profile)
        
        try:
            # Create user profile if not provided
            if not user_profile:
                user_profile = {
                    'risk_tolerance': 'moderate',
                    'investment_horizon': 'long_term',
                    'investment_amount': 10000,
                    'experience_level': 'intermediate'
                }
            
            # Prepare comprehensive analysis
            context = self._prepare_analysis_context(stock_data, news_data)
            context['user_profile'] = user_profile
            
            prompt = self._create_autonomous_recommendation_prompt(context)
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self._get_autonomous_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2500,
                temperature=0.6
            )
            
            ai_response = response.choices[0].message.content
            
            return {
                'recommendation': ai_response,
                'confidence_score': self._calculate_confidence_score(stock_data),
                'risk_assessment': self._assess_risk(stock_data),
                'entry_strategy': self._generate_entry_strategy(stock_data),
                'exit_strategy': self._generate_exit_strategy(stock_data),
                'position_sizing': self._calculate_position_sizing(stock_data, user_profile),
                'monitoring_points': self._generate_monitoring_points(stock_data),
                'ticker': stock_data.get('ticker', ''),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error in OpenAI autonomous recommendation: {e}")
            return self.enhanced_advisor.get_autonomous_recommendation(stock_data, news_data, user_profile)
    
    def get_portfolio_recommendations(self, portfolio_data: List[Dict]) -> Dict:
        """Generate comprehensive portfolio-level recommendations"""
        if not self.config.OPENAI_API_KEY:
            return self._get_comprehensive_portfolio_recommendations()
        
        try:
            # Prepare portfolio context
            context = self._prepare_portfolio_context(portfolio_data)
            
            # Create comprehensive prompt
            prompt = f"""
            Analyze this portfolio comprehensively and provide actionable recommendations:
            
            Portfolio Summary:
            {json.dumps(context, indent=2)}
            
            Please provide:
            1. Overall portfolio health assessment (1-10 scale)
            2. Risk analysis and diversification assessment
            3. Specific stocks to buy, sell, or hold with reasons
            4. Portfolio rebalancing recommendations
            5. Sector allocation analysis
            6. Risk management strategies
            7. Performance optimization suggestions
            8. Entry/exit timing for each recommendation
            9. Position sizing recommendations
            10. Monitoring and alert points
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self._get_comprehensive_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            
            return {
                'analysis': ai_response,
                'portfolio_score': self._calculate_portfolio_score(portfolio_data),
                'risk_level': self._assess_portfolio_risk(portfolio_data),
                'diversification_score': self._calculate_diversification_score(portfolio_data),
                'recommendations': self._extract_portfolio_recommendations(ai_response),
                'timestamp': datetime.now().isoformat(),
                'portfolio_count': len(portfolio_data)
            }
            
        except Exception as e:
            self.logger.error(f"Error in portfolio analysis: {e}")
            return self._get_comprehensive_portfolio_recommendations()
    
    def get_market_insights(self, market_news: List[Dict]) -> Dict:
        """Generate comprehensive market insights and actionable recommendations"""
        if not self.config.OPENAI_API_KEY:
            return self._get_comprehensive_market_insights()
        
        try:
            # Prepare news context
            news_summary = []
            for article in market_news[:10]:  # Top 10 articles
                news_summary.append({
                    'title': article.get('title', ''),
                    'sentiment': article.get('sentiment', {}).get('sentiment', 'neutral'),
                    'source': article.get('source', ''),
                    'description': article.get('description', '')
                })
            
            prompt = f"""
            Analyze these market news articles and provide comprehensive insights:
            
            Recent Market News:
            {json.dumps(news_summary, indent=2)}
            
            Please provide:
            1. Key market trends and themes
            2. Sector-specific opportunities and risks
            3. Specific stock recommendations based on news
            4. Market timing suggestions
            5. Risk factors to monitor
            6. Economic indicators to watch
            7. Portfolio positioning recommendations
            8. Entry/exit strategies for different market conditions
            9. Defensive vs. aggressive positioning advice
            10. Long-term vs. short-term opportunities
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self._get_comprehensive_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1200,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            
            return {
                'insights': ai_response,
                'market_sentiment': self._calculate_market_sentiment(market_news),
                'trending_sectors': self._identify_trending_sectors(market_news),
                'risk_level': self._assess_market_risk(market_news),
                'opportunities': self._extract_opportunities(ai_response),
                'timestamp': datetime.now().isoformat(),
                'news_count': len(market_news)
            }
            
        except Exception as e:
            self.logger.error(f"Error in market insights: {e}")
            return self._get_comprehensive_market_insights()
    
    def _prepare_analysis_context(self, stock_data: Dict, news_data: List[Dict]) -> Dict:
        """Prepare comprehensive context for AI analysis"""
        return {
            'ticker': stock_data.get('ticker', ''),
            'current_price': stock_data.get('current_price', 0),
            'market_cap': stock_data.get('market_cap', 0),
            'fundamental_score': stock_data.get('fundamental_score', 0),
            'technical_score': stock_data.get('technical_score', 0),
            'overall_score': stock_data.get('overall_score', 0),
            'recommendation': stock_data.get('recommendation', ''),
            'fundamental_reasons': stock_data.get('fundamental_reasons', []),
            'technical_reasons': stock_data.get('technical_reasons', []),
            'fundamental_metrics': stock_data.get('fundamental_metrics', {}),
            'technical_indicators': stock_data.get('technical_indicators', {}),
            'recent_news': news_data[:5] if news_data else [],
            'volume': stock_data.get('volume', 0),
            'beta': stock_data.get('fundamental_metrics', {}).get('beta', 0)
        }
    
    def _create_comprehensive_analysis_prompt(self, context: Dict) -> str:
        """Create comprehensive analysis prompt for AI"""
        return f"""
        Provide a comprehensive investment analysis for {context['ticker']} that a user can act on without additional research:
        
        Stock: {context['ticker']}
        Current Price: ${context['current_price']:,.2f}
        Market Cap: ${context['market_cap']:,.0f}
        Overall Score: {context['overall_score']}/100
        Recommendation: {context['recommendation']}
        
        Fundamental Analysis (Score: {context['fundamental_score']}/100):
        - Strengths: {', '.join(context['fundamental_reasons'])}
        - Key Metrics: {json.dumps(context['fundamental_metrics'], indent=2)}
        
        Technical Analysis (Score: {context['technical_score']}/100):
        - Signals: {', '.join(context['technical_reasons'])}
        - Indicators: {json.dumps(context['technical_indicators'], indent=2)}
        
        Recent News: {len(context['recent_news'])} articles
        
        Please provide:
        1. EXECUTIVE SUMMARY: 2-3 sentence investment thesis
        2. INVESTMENT RECOMMENDATION: Buy/Hold/Sell with confidence level
        3. ENTRY STRATEGY: Specific price points and timing
        4. EXIT STRATEGY: Profit targets and stop losses
        5. POSITION SIZING: Recommended allocation percentage
        6. RISK ASSESSMENT: Key risks and mitigation strategies
        7. TIMELINE: Short-term (1-3 months) and long-term (1-3 years) outlook
        8. MONITORING: Key metrics and events to watch
        9. COMPETITIVE ADVANTAGES: Sustainable moats and competitive position
        10. CATALYSTS: Upcoming events that could move the stock
        11. ALTERNATIVES: Similar stocks to consider
        12. ACTION PLAN: Step-by-step implementation guide
        """
    
    def _create_autonomous_recommendation_prompt(self, context: Dict) -> str:
        """Create autonomous recommendation prompt"""
        user_profile = context.get('user_profile', {})
        
        return f"""
        Provide a complete, actionable investment recommendation for {context['ticker']} that requires NO additional research from the user:
        
        USER PROFILE:
        - Risk Tolerance: {user_profile.get('risk_tolerance', 'moderate')}
        - Investment Horizon: {user_profile.get('investment_horizon', 'long_term')}
        - Investment Amount: ${user_profile.get('investment_amount', 10000):,.0f}
        - Experience Level: {user_profile.get('experience_level', 'intermediate')}
        
        STOCK ANALYSIS:
        - Overall Score: {context['overall_score']}/100
        - Recommendation: {context['recommendation']}
        - Current Price: ${context['current_price']:,.2f}
        - Market Cap: ${context['market_cap']:,.0f}
        
        Provide a COMPLETE investment decision including:
        1. FINAL VERDICT: Buy/Hold/Sell with specific reasoning
        2. ENTRY POINTS: Exact price levels to buy (if applicable)
        3. POSITION SIZE: Specific dollar amount or percentage
        4. STOP LOSS: Exact price to sell if wrong
        5. PROFIT TARGETS: Specific price targets for partial and full exits
        6. TIMELINE: When to expect results
        7. RISK REWARD: Expected return vs. potential loss
        8. IMPLEMENTATION: Step-by-step action plan
        9. MONITORING: What to watch and when to adjust
        10. BACKUP PLAN: What to do if the thesis changes
        
        Make this recommendation so complete that the user can implement it immediately without any additional research.
        """
    
    def _get_comprehensive_system_prompt(self) -> str:
        """Get comprehensive system prompt for AI"""
        return """
        You are an expert investment advisor with 20+ years of experience. You provide comprehensive, actionable investment analysis that users can implement immediately without additional research.
        
        Your analysis should be:
        - COMPREHENSIVE: Cover all aspects of the investment decision
        - ACTIONABLE: Provide specific prices, amounts, and timelines
        - RISK-AWARE: Always consider downside scenarios
        - EVIDENCE-BASED: Support recommendations with data
        - USER-FRIENDLY: Clear, jargon-free explanations
        - COMPLETE: No additional research required from user
        
        Follow proven investment principles:
        - The Motley Fool's 8-step process
        - Warren Buffett's value investing principles
        - Modern portfolio theory
        - Risk management best practices
        
        Always provide specific, actionable recommendations with exact numbers, prices, and timelines.
        """
    
    def _get_autonomous_system_prompt(self) -> str:
        """Get autonomous system prompt for AI"""
        return """
        You are a senior investment advisor providing COMPLETE, autonomous investment recommendations. Your goal is to give users everything they need to make an investment decision without requiring any additional research.
        
        Your recommendations must include:
        - Specific buy/sell/hold decision with exact reasoning
        - Precise entry and exit prices
        - Exact position sizing recommendations
        - Complete risk management plan
        - Step-by-step implementation guide
        - Monitoring and adjustment criteria
        
        Make your recommendations so comprehensive that users can implement them immediately with confidence. Include all necessary details: exact prices, amounts, timelines, and contingency plans.
        
        Remember: The user should NOT need to do any additional research after reading your recommendation.
        """
    
    def _parse_comprehensive_ai_response(self, response: str, stock_data: Dict) -> Dict:
        """Parse AI response into structured format"""
        return {
            'ai_analysis': response,
            'ticker': stock_data.get('ticker', ''),
            'timestamp': datetime.now().isoformat(),
            'recommendation': stock_data.get('recommendation', ''),
            'overall_score': stock_data.get('overall_score', 0)
        }
    
    def _get_comprehensive_analysis(self, stock_data: Dict) -> Dict:
        """Get comprehensive analysis without AI"""
        ticker = stock_data.get('ticker', '')
        score = stock_data.get('overall_score', 0)
        price = stock_data.get('current_price', 0)
        
        if score >= 80:
            analysis = f"""
            **STRONG BUY RECOMMENDATION for {ticker}**
            
            **Investment Thesis:**
            {ticker} demonstrates exceptional fundamentals and technical strength, making it an attractive long-term investment opportunity.
            
            **Key Strengths:**
            - Strong competitive advantages and market position
            - Excellent financial metrics and growth potential
            - Positive technical indicators and momentum
            - Favorable risk-reward profile
            
            **Entry Strategy:**
            - Immediate entry at current price: ${price:,.2f}
            - Dollar-cost average on pullbacks to ${price*0.95:,.2f}
            - Position size: 15-25% of portfolio
            
            **Exit Strategy:**
            - Stop loss: ${price*0.85:,.2f} (-15%)
            - Profit targets: ${price*1.15:,.2f}, ${price*1.25:,.2f}, ${price*1.40:,.2f}
            - Timeline: 1-3 years for full potential
            
            **Risk Assessment:**
            - Market volatility and economic uncertainty
            - Sector-specific risks
            - Company execution risk
            
            **Monitoring:**
            - Track quarterly earnings and guidance
            - Monitor technical indicators weekly
            - Watch for sector rotation and market sentiment
            """
        elif score >= 70:
            analysis = f"""
            **BUY RECOMMENDATION for {ticker}**
            
            **Investment Thesis:**
            {ticker} shows solid fundamentals with good growth potential, suitable for moderate risk tolerance.
            
            **Key Strengths:**
            - Good competitive position and financial health
            - Positive growth outlook and reasonable valuation
            - Favorable technical trends
            
            **Entry Strategy:**
            - Consider entry at current price: ${price:,.2f}
            - Wait for pullback to ${price*0.90:,.2f} for better entry
            - Position size: 10-20% of portfolio
            
            **Exit Strategy:**
            - Stop loss: ${price*0.85:,.2f} (-15%)
            - Profit targets: ${price*1.10:,.2f}, ${price*1.20:,.2f}
            - Timeline: 6-18 months
            
            **Risk Assessment:**
            - Moderate market and company-specific risks
            - Sector competition and economic factors
            
            **Monitoring:**
            - Quarterly earnings and guidance
            - Technical support and resistance levels
            - Sector performance and market trends
            """
        else:
            analysis = f"""
            **HOLD/AVOID RECOMMENDATION for {ticker}**
            
            **Analysis:**
            {ticker} shows mixed signals with moderate risk and limited upside potential.
            
            **Concerns:**
            - Suboptimal fundamentals or technical indicators
            - Higher risk relative to potential reward
            - Better opportunities likely available
            
            **Recommendation:**
            - Avoid new positions at current levels
            - Consider selling existing positions if held
            - Monitor for improvement in fundamentals
            
            **Alternative Strategy:**
            - Look for better opportunities in the same sector
            - Consider index funds for broader exposure
            - Wait for significant improvement in metrics
            """
        
        return {
            'ai_analysis': analysis,
            'ticker': ticker,
            'timestamp': datetime.now().isoformat(),
            'recommendation': stock_data.get('recommendation', ''),
            'overall_score': score
        }
    
    def _get_autonomous_fallback_analysis(self, stock_data: Dict, user_profile: Dict) -> Dict:
        """Get autonomous fallback analysis"""
        ticker = stock_data.get('ticker', '')
        score = stock_data.get('overall_score', 0)
        price = stock_data.get('current_price', 0)
        
        if score >= 75:
            decision = "BUY"
            confidence = "High"
            position_size = "15-25% of portfolio"
        elif score >= 60:
            decision = "BUY"
            confidence = "Moderate"
            position_size = "10-15% of portfolio"
        elif score >= 45:
            decision = "HOLD"
            confidence = "Low"
            position_size = "5-10% of portfolio"
        else:
            decision = "SELL"
            confidence = "High"
            position_size = "0% - avoid"
        
        return {
            'recommendation': f"""
            **AUTONOMOUS RECOMMENDATION: {decision} {ticker}**
            
            **Confidence Level: {confidence}**
            **Position Size: {position_size}**
            
            **Entry Strategy:**
            - Current Price: ${price:,.2f}
            - Recommended Entry: ${price:,.2f}
            - Stop Loss: ${price*0.85:,.2f}
            
            **Exit Strategy:**
            - Profit Target 1: ${price*1.15:,.2f}
            - Profit Target 2: ${price*1.25:,.2f}
            - Timeline: 6-12 months
            
            **Implementation:**
            1. Place limit order at recommended entry
            2. Set stop loss immediately
            3. Monitor weekly for adjustments
            4. Take profits at target levels
            
            **Risk Management:**
            - Maximum loss: 15% of position
            - Diversify across sectors
            - Regular portfolio rebalancing
            """,
            'confidence_score': score / 100,
            'risk_assessment': self._assess_risk(stock_data),
            'entry_strategy': self._generate_entry_strategy(stock_data),
            'exit_strategy': self._generate_exit_strategy(stock_data),
            'position_sizing': self._calculate_position_sizing(stock_data, user_profile),
            'monitoring_points': self._generate_monitoring_points(stock_data),
            'ticker': ticker,
            'timestamp': datetime.now().isoformat()
        }
    
    def _get_comprehensive_portfolio_recommendations(self) -> Dict:
        """Get comprehensive portfolio recommendations"""
        return {
            'analysis': """
            **PORTFOLIO OPTIMIZATION RECOMMENDATIONS**
            
            **Overall Assessment:**
            Your portfolio shows good diversification with room for optimization.
            
            **Key Recommendations:**
            1. Rebalance to target allocations
            2. Add defensive positions for risk management
            3. Consider sector rotation opportunities
            4. Monitor high-beta positions closely
            
            **Action Items:**
            - Review positions with scores below 60
            - Add more defensive stocks (utilities, consumer staples)
            - Consider international exposure
            - Implement stop-losses on all positions
            
            **Risk Management:**
            - Maintain 10-15% cash for opportunities
            - Limit individual positions to 5-10%
            - Regular rebalancing (quarterly)
            - Monitor correlation between holdings
            """,
            'portfolio_score': 75,
            'risk_level': 'Moderate',
            'diversification_score': 70,
            'recommendations': ['Rebalance portfolio', 'Add defensive positions', 'Monitor high-risk stocks'],
            'timestamp': datetime.now().isoformat(),
            'portfolio_count': 0
        }
    
    def _get_comprehensive_market_insights(self) -> Dict:
        """Get comprehensive market insights"""
        return {
            'insights': """
            **MARKET INSIGHTS & OPPORTUNITIES**
            
            **Current Market Trends:**
            - Technology sector leading gains
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
            
            **Actionable Recommendations:**
            1. Focus on companies with strong competitive advantages
            2. Maintain defensive positions (utilities, consumer staples)
            3. Consider dollar-cost averaging into quality stocks
            4. Monitor for sector rotation opportunities
            """,
            'market_sentiment': 'Neutral to Positive',
            'trending_sectors': ['Technology', 'Healthcare', 'Financial Services'],
            'risk_level': 'Moderate',
            'opportunities': ['Quality growth stocks', 'Defensive positions', 'Sector rotation'],
            'timestamp': datetime.now().isoformat(),
            'news_count': 0
        }
    
    def _prepare_portfolio_context(self, portfolio_data: List[Dict]) -> Dict:
        """Prepare portfolio context for AI"""
        total_value = sum(item.get('current_price', 0) * item.get('shares', 0) for item in portfolio_data)
        avg_score = sum(item.get('overall_score', 0) for item in portfolio_data) / len(portfolio_data) if portfolio_data else 0
        
        return {
            'total_stocks': len(portfolio_data),
            'total_value': total_value,
            'average_score': avg_score,
            'stocks': [
                {
                    'ticker': item.get('ticker', ''),
                    'score': item.get('overall_score', 0),
                    'recommendation': item.get('recommendation', ''),
                    'weight': (item.get('current_price', 0) * item.get('shares', 0)) / total_value if total_value > 0 else 0
                }
                for item in portfolio_data
            ]
        }
    
    # Helper methods for portfolio analysis
    def _calculate_portfolio_score(self, portfolio_data: List[Dict]) -> float:
        """Calculate overall portfolio score"""
        if not portfolio_data:
            return 0
        scores = [stock.get('overall_score', 0) for stock in portfolio_data]
        return sum(scores) / len(scores)
    
    def _assess_portfolio_risk(self, portfolio_data: List[Dict]) -> str:
        """Assess portfolio risk level"""
        avg_score = self._calculate_portfolio_score(portfolio_data)
        if avg_score >= 70:
            return "Low"
        elif avg_score >= 50:
            return "Moderate"
        else:
            return "High"
    
    def _calculate_diversification_score(self, portfolio_data: List[Dict]) -> float:
        """Calculate diversification score"""
        if len(portfolio_data) < 5:
            return 50  # Need more stocks for good diversification
        elif len(portfolio_data) < 10:
            return 70
        else:
            return 85
    
    def _extract_portfolio_recommendations(self, analysis: str) -> List[str]:
        """Extract portfolio recommendations from analysis"""
        # Simple extraction - in practice, this would be more sophisticated
        recommendations = []
        if "rebalance" in analysis.lower():
            recommendations.append("Rebalance portfolio")
        if "defensive" in analysis.lower():
            recommendations.append("Add defensive positions")
        if "monitor" in analysis.lower():
            recommendations.append("Monitor high-risk positions")
        return recommendations
    
    # Helper methods for market analysis
    def _calculate_market_sentiment(self, market_news: List[Dict]) -> str:
        """Calculate market sentiment from news"""
        if not market_news:
            return "Neutral"
        
        positive_count = sum(1 for article in market_news if article.get('sentiment', {}).get('sentiment') == 'positive')
        negative_count = sum(1 for article in market_news if article.get('sentiment', {}).get('sentiment') == 'negative')
        
        if positive_count > negative_count * 1.5:
            return "Positive"
        elif negative_count > positive_count * 1.5:
            return "Negative"
        else:
            return "Neutral"
    
    def _identify_trending_sectors(self, market_news: List[Dict]) -> List[str]:
        """Identify trending sectors from news"""
        # This would be more sophisticated in practice
        return ["Technology", "Healthcare", "Financial Services"]
    
    def _assess_market_risk(self, market_news: List[Dict]) -> str:
        """Assess market risk level"""
        sentiment = self._calculate_market_sentiment(market_news)
        if sentiment == "Negative":
            return "High"
        elif sentiment == "Neutral":
            return "Moderate"
        else:
            return "Low"
    
    def _extract_opportunities(self, analysis: str) -> List[str]:
        """Extract opportunities from analysis"""
        opportunities = []
        if "tech" in analysis.lower():
            opportunities.append("Technology stocks")
        if "defensive" in analysis.lower():
            opportunities.append("Defensive positions")
        if "quality" in analysis.lower():
            opportunities.append("Quality growth stocks")
        return opportunities
    
    def _calculate_confidence_score(self, stock_data: Dict) -> float:
        """Calculate confidence score for recommendation"""
        score = stock_data.get('overall_score', 0)
        
        if score >= 80:
            return 0.9
        elif score >= 70:
            return 0.8
        elif score >= 60:
            return 0.7
        elif score >= 50:
            return 0.6
        else:
            return 0.4
    
    def _assess_risk(self, stock_data: Dict) -> Dict:
        """Assess investment risk"""
        beta = stock_data.get('fundamental_metrics', {}).get('beta', 1.0)
        score = stock_data.get('overall_score', 50)
        
        if beta > 1.5:
            risk_level = "High"
        elif beta > 1.0:
            risk_level = "Moderate-High"
        elif beta > 0.8:
            risk_level = "Moderate"
        else:
            risk_level = "Low"
        
        return {
            'risk_level': risk_level,
            'beta': beta,
            'volatility': "High" if beta > 1.2 else "Moderate" if beta > 0.8 else "Low",
            'score_risk': "Low" if score >= 70 else "Moderate" if score >= 50 else "High"
        }
    
    def _generate_entry_strategy(self, stock_data: Dict) -> Dict:
        """Generate entry strategy"""
        current_price = stock_data.get('current_price', 0)
        
        return {
            'immediate_entry': current_price,
            'dollar_cost_average': current_price * 0.95,
            'limit_orders': [
                current_price * 0.90,
                current_price * 0.85,
                current_price * 0.80
            ],
            'entry_timing': "Immediate" if stock_data.get('overall_score', 0) >= 70 else "Wait for pullback"
        }
    
    def _generate_exit_strategy(self, stock_data: Dict) -> Dict:
        """Generate exit strategy"""
        current_price = stock_data.get('current_price', 0)
        
        return {
            'stop_loss': current_price * 0.85,
            'profit_targets': [
                current_price * 1.15,
                current_price * 1.25,
                current_price * 1.40
            ],
            'time_based_exits': {
                '3_months': current_price * 1.10,
                '6_months': current_price * 1.20,
                '1_year': current_price * 1.35
            }
        }
    
    def _calculate_position_sizing(self, stock_data: Dict, user_profile: Dict) -> Dict:
        """Calculate position sizing recommendation"""
        investment_amount = user_profile.get('investment_amount', 10000)
        risk_tolerance = user_profile.get('risk_tolerance', 'moderate')
        score = stock_data.get('overall_score', 50)
        
        # Base position size on score and risk tolerance
        if score >= 80:
            base_percentage = 0.15 if risk_tolerance == 'conservative' else 0.25 if risk_tolerance == 'moderate' else 0.35
        elif score >= 70:
            base_percentage = 0.10 if risk_tolerance == 'conservative' else 0.20 if risk_tolerance == 'moderate' else 0.30
        elif score >= 60:
            base_percentage = 0.05 if risk_tolerance == 'conservative' else 0.15 if risk_tolerance == 'moderate' else 0.25
        else:
            base_percentage = 0.02 if risk_tolerance == 'conservative' else 0.10 if risk_tolerance == 'moderate' else 0.20
        
        position_amount = investment_amount * base_percentage
        
        return {
            'percentage': base_percentage * 100,
            'dollar_amount': position_amount,
            'shares': int(position_amount / stock_data.get('current_price', 1)),
            'max_position': min(base_percentage * 2, 0.30) * 100  # Max 30% in any single stock
        }
    
    def _generate_monitoring_points(self, stock_data: Dict) -> List[Dict]:
        """Generate monitoring points"""
        return [
            {
                'metric': 'Price',
                'frequency': 'Daily',
                'alert_levels': [
                    stock_data.get('current_price', 0) * 0.90,
                    stock_data.get('current_price', 0) * 1.15
                ]
            },
            {
                'metric': 'Earnings',
                'frequency': 'Quarterly',
                'next_date': 'Check company calendar'
            },
            {
                'metric': 'Technical Indicators',
                'frequency': 'Weekly',
                'indicators': ['RSI', 'Moving Averages', 'Volume']
            },
            {
                'metric': 'News Sentiment',
                'frequency': 'Daily',
                'sources': ['Financial News', 'Company Press Releases']
            }
        ] 