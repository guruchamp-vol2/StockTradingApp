import json
import random
from typing import Dict, List, Optional
import logging
from datetime import datetime
import re

class LocalAIAdvisor:
    """Local AI advisor that works without OpenAI API - completely free!"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Investment knowledge base
        self.investment_principles = {
            'fundamental_analysis': [
                'Strong competitive advantages and moats',
                'Consistent revenue and earnings growth',
                'Healthy balance sheet with low debt',
                'Strong return on equity (ROE > 15%)',
                'Reasonable valuation (P/E < 30)',
                'Positive cash flow generation',
                'Experienced and aligned management team',
                'Growing market opportunity'
            ],
            'technical_analysis': [
                'Price above key moving averages',
                'Positive momentum indicators',
                'Volume supporting price action',
                'Breakout from resistance levels',
                'RSI not overbought (>30 and <70)',
                'MACD showing positive crossover',
                'Bollinger Bands showing strength',
                'Support levels holding'
            ],
            'risk_management': [
                'Diversify across sectors',
                'Limit individual positions to 5-10%',
                'Set stop losses at 15-20% below entry',
                'Take partial profits at 25% and 50% gains',
                'Monitor quarterly earnings',
                'Watch for sector rotation',
                'Maintain cash reserves',
                'Review positions monthly'
            ]
        }
        
        # Stock analysis templates
        self.analysis_templates = {
            'strong_buy': {
                'recommendation': 'STRONG_BUY',
                'confidence': 0.85,
                'reasoning': [
                    'Exceptional fundamentals with strong competitive advantages',
                    'Excellent technical indicators showing momentum',
                    'Favorable risk-reward profile with multiple catalysts',
                    'Strong management team with proven track record',
                    'Growing market opportunity with sustainable moats'
                ],
                'entry_strategy': 'Immediate entry recommended',
                'position_size': '15-25% of portfolio',
                'timeline': '1-3 years for full potential'
            },
            'buy': {
                'recommendation': 'BUY',
                'confidence': 0.75,
                'reasoning': [
                    'Solid fundamentals with good growth prospects',
                    'Positive technical trends and momentum',
                    'Reasonable valuation with upside potential',
                    'Strong competitive position in growing market',
                    'Experienced management team'
                ],
                'entry_strategy': 'Consider entry on pullbacks',
                'position_size': '10-15% of portfolio',
                'timeline': '6-18 months for results'
            },
            'hold': {
                'recommendation': 'HOLD',
                'confidence': 0.60,
                'reasoning': [
                    'Mixed signals with moderate growth potential',
                    'Fair valuation with limited upside',
                    'Some competitive advantages but risks present',
                    'Wait for better entry point or catalysts',
                    'Monitor for improvement in fundamentals'
                ],
                'entry_strategy': 'Wait for better entry point',
                'position_size': '5-10% of portfolio',
                'timeline': 'Monitor for catalysts'
            },
            'sell': {
                'recommendation': 'SELL',
                'confidence': 0.70,
                'reasoning': [
                    'Deteriorating fundamentals or competitive position',
                    'Negative technical indicators and momentum',
                    'Overvalued relative to growth prospects',
                    'Management concerns or strategic issues',
                    'Better opportunities available elsewhere'
                ],
                'entry_strategy': 'Avoid new positions',
                'position_size': '0% - consider selling existing',
                'timeline': 'Immediate action recommended'
            }
        }
    
    def get_stock_analysis(self, stock_data: Dict, news_data: List[Dict]) -> Dict:
        """Generate comprehensive stock analysis using local AI"""
        try:
            # Analyze stock data
            analysis = self._analyze_stock_data(stock_data)
            
            # Add news sentiment
            if news_data:
                news_sentiment = self._analyze_news_sentiment(news_data)
                analysis['news_impact'] = news_sentiment
            
            # Generate recommendation
            recommendation = self._generate_recommendation(analysis)
            
            return {
                'ai_analysis': self._format_analysis(analysis, recommendation),
                'ticker': stock_data.get('ticker', ''),
                'timestamp': datetime.now().isoformat(),
                'recommendation': recommendation['recommendation'],
                'confidence': recommendation['confidence']
            }
            
        except Exception as e:
            self.logger.error(f"Error in local AI analysis: {e}")
            return self._get_fallback_analysis(stock_data)
    
    def get_autonomous_recommendation(self, stock_data: Dict, news_data: List[Dict], user_profile: Dict = None) -> Dict:
        """Generate autonomous investment recommendation"""
        try:
            # Create user profile if not provided
            if not user_profile:
                user_profile = {
                    'risk_tolerance': 'moderate',
                    'investment_horizon': 'long_term',
                    'investment_amount': 10000,
                    'experience_level': 'intermediate'
                }
            
            # Analyze stock comprehensively
            analysis = self._analyze_stock_data(stock_data)
            
            # Add news analysis
            if news_data:
                news_sentiment = self._analyze_news_sentiment(news_data)
                analysis['news_sentiment'] = news_sentiment
            
            # Generate recommendation
            recommendation = self._generate_recommendation(analysis)
            
            # Calculate position sizing
            position_sizing = self._calculate_position_sizing(stock_data, user_profile, recommendation)
            
            # Generate entry/exit strategy
            entry_strategy = self._generate_entry_strategy(stock_data, recommendation)
            exit_strategy = self._generate_exit_strategy(stock_data, recommendation)
            
            return {
                'recommendation': self._format_autonomous_recommendation(
                    stock_data, recommendation, position_sizing, entry_strategy, exit_strategy, user_profile
                ),
                'confidence_score': recommendation['confidence'],
                'risk_assessment': self._assess_risk(stock_data),
                'entry_strategy': entry_strategy,
                'exit_strategy': exit_strategy,
                'position_sizing': position_sizing,
                'monitoring_points': self._generate_monitoring_points(stock_data),
                'ticker': stock_data.get('ticker', ''),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error in autonomous recommendation: {e}")
            return self._get_autonomous_fallback(stock_data, user_profile)
    
    def _analyze_stock_data(self, stock_data: Dict) -> Dict:
        """Analyze stock data using local AI rules"""
        analysis = {
            'fundamental_score': stock_data.get('fundamental_score', 0),
            'technical_score': stock_data.get('technical_score', 0),
            'overall_score': stock_data.get('overall_score', 0),
            'strengths': [],
            'weaknesses': [],
            'opportunities': [],
            'threats': []
        }
        
        # Analyze fundamental metrics
        metrics = stock_data.get('fundamental_metrics', {})
        
        if metrics.get('pe_ratio', 0) > 0 and metrics.get('pe_ratio', 0) < 30:
            analysis['strengths'].append('Reasonable P/E ratio')
        elif metrics.get('pe_ratio', 0) > 50:
            analysis['weaknesses'].append('High P/E ratio - may be overvalued')
        
        if metrics.get('roe', 0) > 0.15:
            analysis['strengths'].append('Strong return on equity')
        elif metrics.get('roe', 0) < 0.10:
            analysis['weaknesses'].append('Low return on equity')
        
        if metrics.get('debt_to_equity', 0) < 0.5:
            analysis['strengths'].append('Low debt levels')
        elif metrics.get('debt_to_equity', 0) > 1.0:
            analysis['weaknesses'].append('High debt levels')
        
        # Analyze technical indicators
        indicators = stock_data.get('technical_indicators', {})
        
        if indicators.get('rsi', 0) > 30 and indicators.get('rsi', 0) < 70:
            analysis['strengths'].append('RSI in healthy range')
        elif indicators.get('rsi', 0) > 70:
            analysis['weaknesses'].append('RSI overbought')
        
        if indicators.get('price_vs_ma20', 0) > 0:
            analysis['strengths'].append('Price above 20-day moving average')
        else:
            analysis['weaknesses'].append('Price below 20-day moving average')
        
        # Generate opportunities and threats
        if analysis['overall_score'] >= 80:
            analysis['opportunities'].append('Strong growth potential')
            analysis['opportunities'].append('Market leadership position')
        elif analysis['overall_score'] >= 60:
            analysis['opportunities'].append('Moderate growth potential')
        else:
            analysis['threats'].append('Limited growth potential')
            analysis['threats'].append('Competitive pressures')
        
        return analysis
    
    def _analyze_news_sentiment(self, news_data: List[Dict]) -> Dict:
        """Analyze news sentiment"""
        if not news_data:
            return {'sentiment': 'neutral', 'score': 0.5, 'impact': 'minimal'}
        
        # Calculate average sentiment
        sentiments = []
        for article in news_data:
            sentiment = article.get('sentiment', {}).get('polarity', 0)
            sentiments.append(sentiment)
        
        avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0
        
        if avg_sentiment > 0.1:
            sentiment_category = 'positive'
            impact = 'favorable'
        elif avg_sentiment < -0.1:
            sentiment_category = 'negative'
            impact = 'unfavorable'
        else:
            sentiment_category = 'neutral'
            impact = 'minimal'
        
        return {
            'sentiment': sentiment_category,
            'score': avg_sentiment,
            'impact': impact,
            'article_count': len(news_data)
        }
    
    def _generate_recommendation(self, analysis: Dict) -> Dict:
        """Generate investment recommendation based on analysis"""
        score = analysis['overall_score']
        
        if score >= 80:
            template = self.analysis_templates['strong_buy']
        elif score >= 70:
            template = self.analysis_templates['buy']
        elif score >= 50:
            template = self.analysis_templates['hold']
        else:
            template = self.analysis_templates['sell']
        
        return template.copy()
    
    def _calculate_position_sizing(self, stock_data: Dict, user_profile: Dict, recommendation: Dict) -> Dict:
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
        current_price = stock_data.get('current_price', 1)
        
        return {
            'percentage': base_percentage * 100,
            'dollar_amount': position_amount,
            'shares': int(position_amount / current_price) if current_price > 0 else 0,
            'max_position': min(base_percentage * 2, 0.30) * 100
        }
    
    def _generate_entry_strategy(self, stock_data: Dict, recommendation: Dict) -> Dict:
        """Generate entry strategy"""
        current_price = stock_data.get('current_price', 0)
        
        if recommendation['recommendation'] in ['STRONG_BUY', 'BUY']:
            entry_timing = 'Immediate entry recommended'
            dollar_cost_average = current_price * 0.95
        else:
            entry_timing = 'Wait for better entry point'
            dollar_cost_average = current_price * 0.90
        
        return {
            'immediate_entry': current_price,
            'dollar_cost_average': dollar_cost_average,
            'limit_orders': [
                current_price * 0.90,
                current_price * 0.85,
                current_price * 0.80
            ],
            'entry_timing': entry_timing
        }
    
    def _generate_exit_strategy(self, stock_data: Dict, recommendation: Dict) -> Dict:
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
    
    def _format_analysis(self, analysis: Dict, recommendation: Dict) -> str:
        """Format analysis for display"""
        ticker = analysis.get('ticker', 'STOCK')
        
        return f"""
**COMPREHENSIVE ANALYSIS for {ticker}**

**Investment Thesis:**
{recommendation['reasoning'][0]}

**Key Strengths:**
{chr(10).join(f"• {strength}" for strength in analysis['strengths'][:3])}

**Key Concerns:**
{chr(10).join(f"• {weakness}" for weakness in analysis['weaknesses'][:2])}

**Entry Strategy:**
• {recommendation['entry_strategy']}
• Position Size: {recommendation['position_size']}

**Exit Strategy:**
• Stop Loss: 15% below entry
• Profit Targets: 25%, 50%, and 100% gains
• Timeline: {recommendation['timeline']}

**Risk Assessment:**
• Overall Risk: {'Low' if analysis['overall_score'] >= 70 else 'Moderate' if analysis['overall_score'] >= 50 else 'High'}
• Volatility: {'Low' if analysis.get('fundamental_metrics', {}).get('beta', 1) < 1 else 'Moderate' if analysis.get('fundamental_metrics', {}).get('beta', 1) < 1.5 else 'High'}

**Monitoring Points:**
• Track quarterly earnings and guidance
• Monitor technical indicators weekly
• Watch for sector rotation and market sentiment
• Review position monthly for adjustments
"""
    
    def _format_autonomous_recommendation(self, stock_data: Dict, recommendation: Dict, position_sizing: Dict, entry_strategy: Dict, exit_strategy: Dict, user_profile: Dict) -> str:
        """Format autonomous recommendation"""
        ticker = stock_data.get('ticker', 'STOCK')
        current_price = stock_data.get('current_price', 0)
        
        return f"""
**🎯 AUTONOMOUS INVESTMENT RECOMMENDATION: {recommendation['recommendation']} {ticker}**

**Confidence Level: {recommendation['confidence']:.1%}**
**Position Size: {position_sizing['percentage']:.1f}% of portfolio**

**Entry Strategy:**
• Current Price: ${current_price:,.2f}
• Recommended Entry: ${entry_strategy['immediate_entry']:,.2f}
• Stop Loss: ${exit_strategy['stop_loss']:,.2f}

**Exit Strategy:**
• Profit Target 1: ${exit_strategy['profit_targets'][0]:,.2f}
• Profit Target 2: ${exit_strategy['profit_targets'][1]:,.2f}
• Timeline: 6-12 months

**Implementation:**
1. Place limit order at recommended entry
2. Set stop loss immediately
3. Monitor weekly for adjustments
4. Take profits at target levels

**Risk Management:**
• Maximum loss: 15% of position
• Diversify across sectors
• Regular portfolio rebalancing

**Reasoning:**
{chr(10).join(f"• {reason}" for reason in recommendation['reasoning'][:3])}
"""
    
    def _get_fallback_analysis(self, stock_data: Dict) -> Dict:
        """Get fallback analysis when AI fails"""
        return {
            'ai_analysis': f"""
**BASIC ANALYSIS for {stock_data.get('ticker', 'STOCK')}**

**Score: {stock_data.get('overall_score', 0)}/100**
**Recommendation: {stock_data.get('recommendation', 'HOLD')}**

**Key Metrics:**
• Current Price: ${stock_data.get('current_price', 0):,.2f}
• Market Cap: ${stock_data.get('market_cap', 0):,.0f}
• Fundamental Score: {stock_data.get('fundamental_score', 0)}/100
• Technical Score: {stock_data.get('technical_score', 0)}/100

**Recommendation:**
Based on the available data, this stock shows {'strong' if stock_data.get('overall_score', 0) >= 70 else 'moderate' if stock_data.get('overall_score', 0) >= 50 else 'weak'} fundamentals and technical indicators.

**Action Plan:**
• {'Consider buying' if stock_data.get('overall_score', 0) >= 70 else 'Hold existing positions' if stock_data.get('overall_score', 0) >= 50 else 'Avoid new positions'}
• Set stop loss at 15% below current price
• Monitor quarterly earnings and technical indicators
• Review position monthly
""",
            'ticker': stock_data.get('ticker', ''),
            'timestamp': datetime.now().isoformat(),
            'recommendation': stock_data.get('recommendation', 'HOLD'),
            'overall_score': stock_data.get('overall_score', 0)
        }
    
    def _get_autonomous_fallback(self, stock_data: Dict, user_profile: Dict) -> Dict:
        """Get autonomous fallback recommendation"""
        score = stock_data.get('overall_score', 50)
        
        if score >= 75:
            decision = "BUY"
            confidence = 0.75
            position_size = "15-25% of portfolio"
        elif score >= 60:
            decision = "BUY"
            confidence = 0.65
            position_size = "10-15% of portfolio"
        elif score >= 45:
            decision = "HOLD"
            confidence = 0.55
            position_size = "5-10% of portfolio"
        else:
            decision = "SELL"
            confidence = 0.70
            position_size = "0% - avoid"
        
        return {
            'recommendation': f"""
**AUTONOMOUS RECOMMENDATION: {decision} {stock_data.get('ticker', 'STOCK')}**

**Confidence Level: {confidence:.1%}**
**Position Size: {position_size}**

**Entry Strategy:**
• Current Price: ${stock_data.get('current_price', 0):,.2f}
• Recommended Entry: ${stock_data.get('current_price', 0):,.2f}
• Stop Loss: ${stock_data.get('current_price', 0) * 0.85:,.2f}

**Exit Strategy:**
• Profit Target 1: ${stock_data.get('current_price', 0) * 1.15:,.2f}
• Profit Target 2: ${stock_data.get('current_price', 0) * 1.25:,.2f}
• Timeline: 6-12 months

**Implementation:**
1. Place limit order at recommended entry
2. Set stop loss immediately
3. Monitor weekly for adjustments
4. Take profits at target levels

**Risk Management:**
• Maximum loss: 15% of position
• Diversify across sectors
• Regular portfolio rebalancing
""",
            'confidence_score': confidence,
            'risk_assessment': self._assess_risk(stock_data),
            'entry_strategy': self._generate_entry_strategy(stock_data, {'recommendation': decision}),
            'exit_strategy': self._generate_exit_strategy(stock_data, {'recommendation': decision}),
            'position_sizing': self._calculate_position_sizing(stock_data, user_profile, {'recommendation': decision}),
            'monitoring_points': self._generate_monitoring_points(stock_data),
            'ticker': stock_data.get('ticker', ''),
            'timestamp': datetime.now().isoformat()
        } 