#!/usr/bin/env python3
"""
Setup script for AI Stock Analyzer & Advisor
"""

import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False
    return True

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = Path(".env")
    if not env_file.exists():
        print("🔧 Creating .env file...")
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
    else:
        print("✅ .env file already exists")

def check_dependencies():
    """Check if all required packages are installed"""
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
        return False
    else:
        print("✅ All required packages are installed")
        return True

def main():
    """Main setup function"""
    print("🚀 Setting up AI Stock Analyzer & Advisor...")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Install requirements
    if not install_requirements():
        return
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Please install missing packages manually")
        return
    
    # Create .env file
    create_env_file()
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit .env file with your API keys")
    print("2. Run: streamlit run app.py")
    print("3. Open your browser to the URL shown")
    print("\n🔑 Get API keys from:")
    print("- OpenAI: https://platform.openai.com/api-keys")
    print("- News API: https://newsapi.org/register")
    print("\n⚠️  Disclaimer: This app is for educational purposes only.")
    print("   Always do your own research before making investment decisions.")

if __name__ == "__main__":
    main() 