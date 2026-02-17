#!/usr/bin/env python3
"""
Simplified LLM & NLP Functionality Demo
Demonstrating core features without needing an API key
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_service.ai import NLPProcessor, SentimentFactorCalculator
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging

def setup_logging():
    """Setup logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def demo_nlp_processing():
    """Demonstrate NLP processing features"""
    print("🔍 NLP Processing Demo")
    print("=" * 50)
    
    # Initialize NLP processor
    nlp_processor = NLPProcessor(use_spacy=False, use_transformers=False)
    
    # Sample texts
    sample_texts = [
        "Apple reports strong Q4 earnings, stock surges 5% on better-than-expected iPhone sales",
        "Tesla faces production challenges, shares decline due to supply chain issues",
        "Google announces revolutionary AI breakthrough that could transform the industry",
        "Market volatility increases as investors react to Fed policy changes"
    ]
    
    print("📝 Processing sample texts:")
    for i, text in enumerate(sample_texts, 1):
        print(f"\n{i}. Original: {text}")
        
        # Preprocess text
        processed = nlp_processor.preprocess_text(text)
        
        print(f"   Cleaned: {processed.cleaned_text[:100]}...")
        print(f"   Keywords: {', '.join(processed.keywords[:5])}")
        print(f"   Sentiment: {processed.sentiment_label} (Score: {processed.sentiment_score:.2f})")
        print(f"   Topics: {', '.join(processed.topics[:3])}")

def demo_sentiment_factor():
    """Demonstrate sentiment factor generation"""
    print("\n📊 Sentiment Factor Demo")
    print("=" * 50)
    
    # Initialize sentiment factor calculator
    sentiment_calculator = SentimentFactorCalculator()
    
    # Simulate sentiment data
    sentiment_data = pd.DataFrame({
        'symbol': ['AAPL', 'GOOGL', 'TSLA', 'MSFT', 'AMZN'] * 10,
        'date': pd.date_range('2024-01-01', periods=50, freq='D').repeat(5),
        'sentiment_score': np.random.normal(0, 0.3, 50),
        'volume': np.random.randint(100, 1000, 50),
        'source': ['news', 'twitter', 'reddit'] * 16 + ['news', 'twitter']
    })
    
    print("📈 Generating sentiment factors:")
    
    # Calculate various sentiment factors
    factors = sentiment_calculator.calculate_sentiment_factors(sentiment_data)
    
    for factor_name, factor_data in factors.items():
        if isinstance(factor_data, dict):
            print(f"\n{factor_name}:")
            for symbol, value in list(factor_data.items())[:3]:  # Show first 3
                print(f"  {symbol}: {value:.4f}")
        else:
            print(f"{factor_name}: {factor_data:.4f}")

def demo_market_analysis():
    """Demonstrate market analysis features"""
    print("\n🎯 Market Analysis Demo")
    print("=" * 50)
    
    # Simulate market data
    dates = pd.date_range('2024-01-01', periods=30, freq='D')
    symbols = ['AAPL', 'GOOGL', 'TSLA']
    
    market_data = {}
    for symbol in symbols:
        base_price = np.random.uniform(100, 500)
        returns = np.random.normal(0.001, 0.02, len(dates))
        prices = [base_price]
        
        for ret in returns[1:]:
            prices.append(prices[-1] * (1 + ret))
        
        market_data[symbol] = pd.DataFrame({
            'date': dates,
            'close': prices,
            'volume': np.random.randint(1000000, 10000000, len(dates))
        })
    
    # Simulate sentiment data
    sentiment_data = pd.DataFrame({
        'symbol': symbols * 10,
        'date': pd.date_range('2024-01-01', periods=30, freq='D').repeat(len(symbols)),
        'sentiment_score': np.random.normal(0, 0.3, 30 * len(symbols)),
        'volume': np.random.randint(100, 1000, 30 * len(symbols))
    })
    
    print("📊 Market Analysis Results:")
    
    # Calculate market sentiment indicators
    sentiment_calculator = SentimentFactorCalculator()
    market_sentiment = sentiment_calculator.calculate_market_sentiment(sentiment_data)
    
    print(f"Overall Market Sentiment: {market_sentiment['overall_sentiment']:.2f}")
    print(f"Sentiment Volatility: {market_sentiment['sentiment_volatility']:.4f}")
    print(f"Sentiment Consensus: {market_sentiment['sentiment_consensus']:.2f}")
    
    # Analysis by stock
    print("\nSentiment Analysis by Stock:")
    for symbol in symbols:
        symbol_sentiment = sentiment_data[sentiment_data['symbol'] == symbol]['sentiment_score'].mean()
        print(f"  {symbol}: {symbol_sentiment:.3f}")

def demo_strategy_integration():
    """Demonstrate integration with strategy system"""
    print("\n⚙️ Strategy System Integration Demo")
    print("=" * 50)
    
    # Simulate factor data
    factor_data = pd.DataFrame({
        'symbol': ['AAPL', 'GOOGL', 'TSLA', 'MSFT', 'AMZN'] * 5,
        'date': pd.date_range('2024-01-01', periods=25, freq='D').repeat(5),
        'factor_name': ['sentiment_momentum', 'sentiment_volatility', 'news_volume', 'social_volume', 'sentiment_consensus'] * 5,
        'factor_value': np.random.normal(0, 1, 125)
    })
    
    # Simulate price data
    price_data = pd.DataFrame({
        'symbol': ['AAPL', 'GOOGL', 'TSLA', 'MSFT', 'AMZN'] * 5,
        'date': pd.date_range('2024-01-01', periods=25, freq='D').repeat(5),
        'close': np.random.uniform(100, 500, 125)
    })
    
    print("🔗 Sentiment Factor & Strategy Integration:")
    
    # Calculate sentiment factor weights
    sentiment_factors = factor_data[factor_data['factor_name'].str.contains('sentiment')]
    
    print("Sentiment Factor Statistics:")
    for factor_name in sentiment_factors['factor_name'].unique():
        factor_values = sentiment_factors[sentiment_factors['factor_name'] == factor_name]['factor_value']
        print(f"  {factor_name}: Mean={factor_values.mean():.3f}, Std={factor_values.std():.3f}")
    
    # Simulate strategy signals
    print("\nStrategy Signal Generation:")
    signals = []
    for symbol in ['AAPL', 'GOOGL', 'TSLA']:
        symbol_sentiment = sentiment_factors[sentiment_factors['symbol'] == symbol]['factor_value'].mean()
        
        if symbol_sentiment > 0.5:
            signal = "Strong Buy"
        elif symbol_sentiment > 0:
            signal = "Buy"
        elif symbol_sentiment > -0.5:
            signal = "Hold"
        else:
            signal = "Sell"
        
        signals.append((symbol, symbol_sentiment, signal))
        print(f"  {symbol}: Sentiment Score={symbol_sentiment:.3f} → {signal}")

def main():
    """Main function"""
    setup_logging()
    
    print("🚀 LLM & NLP Extension Module Demo")
    print("=" * 60)
    
    try:
        # Demonstrate various functional modules
        demo_nlp_processing()
        demo_sentiment_factor()
        demo_market_analysis()
        demo_strategy_integration()
        
        print("\n✅ Demo Complete!")
        print("\n📋 Feature Summary:")
        print("  • NLP Text Processing: Cleaning, Tokenization, Keyword Extraction, Sentiment Analysis")
        print("  • Sentiment Factor Generation: Momentum, Volatility, Volume, Consensus")
        print("  • Market Analysis: Overall Sentiment, Stock sentiment, Trend analysis")
        print("  • Strategy Integration: Sentiment factor weighting, Trading signal generation")
        
    except Exception as e:
        print(f"❌ Error occurred during demo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()