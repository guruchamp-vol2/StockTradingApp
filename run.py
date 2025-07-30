#!/usr/bin/env python3
"""
Run script for AI Stock Analyzer & Advisor
"""

import subprocess
import sys
import os
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed"""
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
        print("Please run: python setup.py")
        return False
    
    return True

def check_env_file():
    """Check if .env file exists"""
    if not Path(".env").exists():
        print("⚠️  .env file not found. Creating template...")
        env_content = """# OpenAI API Key for AI-powered analysis
OPENAI_API_KEY=your_openai_api_key_here

# News API Key for financial news
NEWS_API_KEY=your_news_api_key_here

# Alpha Vantage API Key (optional)
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key_here

# Application Settings
DEBUG=True
LOG_LEVEL=INFO
"""
        with open(".env", "w") as f:
            f.write(env_content)
        print("✅ .env file created!")
        print("📝 Please edit .env file with your API keys")
        print("🔑 Get API keys from:")
        print("   - OpenAI: https://platform.openai.com/api-keys")
        print("   - News API: https://newsapi.org/register")
        return False
    
    return True

def main():
    """Main run function"""
    print("🚀 Starting AI Stock Analyzer & Advisor...")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Check environment file
    env_ok = check_env_file()
    
    print("✅ All checks passed!")
    print("🌐 Starting Streamlit app...")
    print("📱 The app will open in your browser")
    print("⚠️  Remember: This is for educational purposes only")
    print("=" * 50)
    
    try:
        # Run streamlit app
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n👋 App stopped by user")
    except Exception as e:
        print(f"❌ Error running app: {e}")
        print("Try running: streamlit run app.py")

if __name__ == "__main__":
    main() 