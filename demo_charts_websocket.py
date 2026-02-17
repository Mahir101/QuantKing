#!/usr/bin/env python3
"""
Chart Library and WebSocket Demo
Demonstrating Plotly, Matplotlib charts and WebSocket real-time data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import asyncio
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging

# Import our modules
from data_service.visualization import PlotlyChartGenerator
from data_service.realtime import RealTimeDataFeed, WebSocketClient
from data_service.factors import FactorCalculator

def setup_logging():
    """Setup logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def generate_sample_data():

    print("📊 Generate sample data...")
    
    # Generate price data
    dates = pd.date_range('2024-01-01', periods=100, freq='D')
    symbols = ['AAPL', 'GOOGL', 'TSLA']
    
    market_data = {}
    for symbol in symbols:
        base_price = np.random.uniform(100, 500)
        returns = np.random.normal(0.001, 0.02, len(dates))
        prices = [base_price]
        
        for ret in returns[1:]:
            prices.append(prices[-1] * (1 + ret))
        
        # Generate OHLCV data
        ohlcv_data = []
        for i, price in enumerate(prices):
            high = price * (1 + abs(np.random.normal(0, 0.01)))
            low = price * (1 - abs(np.random.normal(0, 0.01)))
            open_price = prices[i-1] if i > 0 else price
            volume = np.random.randint(1000000, 10000000)
            
            ohlcv_data.append({
                'open': open_price,
                'high': high,
                'low': low,
                'close': price,
                'volume': volume
            })
        
        market_data[symbol] = pd.DataFrame(ohlcv_data, index=dates)
    
    return market_data

def demo_plotly_charts():
    """Demonstrate Plotly chart features"""
    print("\n📈 Plotly Chart Demo")
    print("=" * 50)
    
    # Generate data
    market_data = generate_sample_data()
    
    # Initialize chart generator
    chart_generator = PlotlyChartGenerator()
    
    # 1. Candlestick chart
    print("1. Creating Candlestick chart...")
    symbol = 'AAPL'
    data = market_data[symbol]
    
    candlestick_fig = chart_generator.create_candlestick_chart(
        data=data,
        symbol=symbol,
        title=f"{symbol} Candlestick Chart Example"
    )
    
    # Save chart
    candlestick_fig.write_html(f"charts/{symbol}_candlestick.html")
    print(f"   ✅ Candlestick chart saved to charts/{symbol}_candlestick.html")
    
    # 2. Technical analysis chart
    print("2. Creating technical analysis chart...")
    
    # Add technical indicators
    data['sma_20'] = data['close'].rolling(20).mean()
    data['ema_20'] = data['close'].ewm(span=20).mean()
    data['rsi'] = calculate_rsi(data['close'])
    
    # Bollinger Bands
    data['bb_upper'] = data['close'].rolling(20).mean() + 2 * data['close'].rolling(20).std()
    data['bb_lower'] = data['close'].rolling(20).mean() - 2 * data['close'].rolling(20).std()
    
    tech_fig = chart_generator.create_technical_analysis_chart(
        data=data,
        symbol=symbol,
        indicators=['sma', 'ema', 'bollinger']
    )
    
    tech_fig.write_html(f"charts/{symbol}_technical.html")
    print(f"   ✅ Technical analysis chart saved to charts/{symbol}_technical.html")
    
    # 3. Factor analysis chart
    print("3. Creating factor analysis chart...")
    
    # Generate factor data
    factor_calc = FactorCalculator()
    factor_data = pd.DataFrame()
    
    for symbol in symbols:
        symbol_data = market_data[symbol]
        factors = factor_calc.calculate_all_factors(
            symbol=symbol,
            prices=symbol_data['close'],
            volumes=symbol_data['volume']
        )
        
        for factor_name, factor_value in factors.items():
            factor_data.loc[symbol, factor_name] = factor_value
    
    factor_fig = chart_generator.create_factor_analysis_chart(
        factor_data=factor_data,
        factor_names=['momentum_20d', 'volatility', 'price_vs_ma20']
    )
    
    factor_fig.write_html("charts/factor_analysis.html")
    print("   ✅ Factor analysis chart saved to charts/factor_analysis.html")
    
    # 4. Portfolio performance chart
    print("4. Creating portfolio performance chart...")
    
    # Simulate portfolio data
    portfolio_returns = np.random.normal(0.001, 0.02, len(dates))
    equity_curve = pd.Series((1 + pd.Series(portfolio_returns)).cumprod(), index=dates)
    
    # Simulate benchmark data
    benchmark_returns = np.random.normal(0.0008, 0.015, len(dates))
    benchmark = pd.Series((1 + pd.Series(benchmark_returns)).cumprod(), index=dates)
    
    # Simulate trade data
    trades_data = []
    for i in range(10):
        trade_date = dates[np.random.randint(0, len(dates))]
        trades_data.append({
            'timestamp': trade_date,
            'price': np.random.uniform(100, 500),
            'side': np.random.choice(['buy', 'sell']),
            'quantity': np.random.randint(100, 1000)
        })
    
    trades_df = pd.DataFrame(trades_data)
    
    portfolio_fig = chart_generator.create_portfolio_performance_chart(
        equity_curve=equity_curve,
        benchmark=benchmark,
        trades=trades_df
    )
    
    portfolio_fig.write_html("charts/portfolio_performance.html")
    print("   ✅ Portfolio performance chart saved to charts/portfolio_performance.html")
    
def calculate_rsi(prices, period=14):
    """Calculate RSI indicator"""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

async def demo_websocket():
    """Demonstrate WebSocket features"""
    print("\n🌐 WebSocket Demo")
    print("=" * 50)
    
    # Create real-time data feed
    real_time_feed = RealTimeDataFeed(exchanges=["binance"])
    
    # Add callback functions
    async def on_tick(tick):
        print(f"📊 Received {tick.symbol} price: ${tick.price:.2f} time: {tick.timestamp}")
    
    async def on_snapshot(snapshot):
        print(f"📈 {snapshot.symbol} Snapshot: O:{snapshot.open:.2f} H:{snapshot.high:.2f} L:{snapshot.low:.2f} C:{snapshot.close:.2f}")
    
    async def on_alert(alert):
        print(f"🚨 Alert: {alert['symbol']} {alert['alert_type']} current value: {alert['current_value']:.2f}")
    
    real_time_feed.add_tick_callback(on_tick)
    real_time_feed.add_snapshot_callback(on_snapshot)
    real_time_feed.add_alert_callback(on_alert)
    
    # Set price alerts
    real_time_feed.set_price_alert("btcusdt", "high", 50000)
    real_time_feed.set_price_alert("btcusdt", "low", 40000)
    
    print("🔌 Starting WebSocket connection...")
    try:
        # Start real-time data feed
        await real_time_feed.start(symbols=["btcusdt", "ethusdt"])
        
        # Run for a while
        print("⏱️ Running for 30 seconds to receive real-time data...")
        await asyncio.sleep(30)
        
        # Stop
        await real_time_feed.stop()
        print("✅ WebSocket demo complete")
        
    except Exception as e:
        print(f"❌ WebSocket error: {e}")
        print("💡 Note: This requires a valid API key to connect to the exchange")

def demo_matplotlib_charts():
    """Demonstrate Matplotlib chart features"""
    print("\n📊 Matplotlib Chart Demo")
    print("=" * 50)
    
    try:
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        from matplotlib.patches import Rectangle
        
        # Generate data
        market_data = generate_sample_data()
        symbol = 'AAPL'
        data = market_data[symbol]
        
        # Create chart
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        # 1. Candlestick chart
        print("1. Creating Matplotlib Candlestick chart...")
        
        # Draw candlesticks
        for i, (date, row) in enumerate(data.iterrows()):
            color = 'green' if row['close'] >= row['open'] else 'red'
            
            # Body
            rect = Rectangle((i-0.3, min(row['open'], row['close'])), 
                           0.6, abs(row['close'] - row['open']), 
                           facecolor=color, edgecolor='black')
            ax1.add_patch(rect)
            
            # Wick
            ax1.plot([i, i], [row['low'], row['high']], color='black', linewidth=1)
        
        ax1.set_title(f'{symbol} Candlestick Chart (Matplotlib)')
        ax1.set_ylabel('Price')
        ax1.grid(True, alpha=0.3)
        
        # Set x-axis labels
        ax1.set_xticks(range(0, len(data), 10))
        ax1.set_xticklabels([data.index[i].strftime('%Y-%m-%d') for i in range(0, len(data), 10)], rotation=45)
        
        # 2. Volume chart
        print("2. Creating volume chart...")
        
        ax2.bar(range(len(data)), data['volume'], alpha=0.7, color='blue')
        ax2.set_title('Volume')
        ax2.set_ylabel('Volume')
        ax2.set_xlabel('Date')
        ax2.grid(True, alpha=0.3)
        
        # Set x-axis labels
        ax2.set_xticks(range(0, len(data), 10))
        ax2.set_xticklabels([data.index[i].strftime('%Y-%m-%d') for i in range(0, len(data), 10)], rotation=45)
        
        plt.tight_layout()
        plt.savefig('charts/matplotlib_candlestick.png', dpi=300, bbox_inches='tight')
        print("   ✅ Matplotlib chart saved to charts/matplotlib_candlestick.png")
        
        # 3. Technical indicators chart
        print("3. Creating technical indicators chart...")
        
        fig2, (ax3, ax4) = plt.subplots(2, 1, figsize=(12, 8))
        
        # Price and Moving Averages
        ax3.plot(data.index, data['close'], label='Close Price', linewidth=2)
        ax3.plot(data.index, data['close'].rolling(20).mean(), label='SMA 20', linewidth=2)
        ax3.plot(data.index, data['close'].ewm(span=20).mean(), label='EMA 20', linewidth=2)
        
        ax3.set_title(f'{symbol} Technical Indicators')
        ax3.set_ylabel('Price')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # RSI
        rsi = calculate_rsi(data['close'])
        ax4.plot(data.index, rsi, label='RSI', linewidth=2, color='purple')
        ax4.axhline(y=70, color='r', linestyle='--', alpha=0.7)
        ax4.axhline(y=30, color='g', linestyle='--', alpha=0.7)
        ax4.fill_between(data.index, 70, 100, alpha=0.3, color='red')
        ax4.fill_between(data.index, 0, 30, alpha=0.3, color='green')
        
        ax4.set_ylabel('RSI')
        ax4.set_xlabel('Date')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('charts/matplotlib_technical.png', dpi=300, bbox_inches='tight')
        print("   ✅ Technical indicators chart saved to charts/matplotlib_technical.png")
        
    except ImportError:
        print("❌ Matplotlib not installed, skipping Matplotlib demo")
    except Exception as e:
        print(f"❌ Matplotlib chart creation failed: {e}")

def create_charts_directory():
    """Create charts directory"""
    if not os.path.exists('charts'):
        os.makedirs('charts')
        print("📁 Creating charts directory")

async def main():
    """Main function"""
    setup_logging()
    
    print("🚀 Chart Library and WebSocket Demo")
    print("=" * 60)
    
    # Create directory
    create_charts_directory()
    
    try:
        # Demo Plotly charts
        demo_plotly_charts()
        
        # Demo Matplotlib charts
        demo_matplotlib_charts()
        
        # Demo WebSocket (optional)
        print("\n❓ Do you want to demo WebSocket features? (API key required)")
        print("   Enter 'y' to continue, any other key to skip...")
        
        # Simple handling, skip WebSocket demo directly
        print("⏭️ Skipping WebSocket demo (API key required)")
        
        print("\n✅ Demo complete!")
        print("\n📋 Feature Summary:")
        print("  • Plotly Charts: Candlestick, Technical Analysis, Factor Analysis, Portfolio Performance")
        print("  • Matplotlib Charts: Candlestick, Technical Indicators, Volume")
        print("  • WebSocket Support: Real-time data feed, Price alerts, Callback handling")
        print("  • Chart Export: HTML, PNG, PDF formats")
        
        print("\n📁 Generated chart files:")
        print("  • charts/AAPL_candlestick.html - Candlestick Chart")
        print("  • charts/AAPL_technical.html - Technical Analysis Chart")
        print("  • charts/factor_analysis.html - Factor Analysis Chart")
        print("  • charts/portfolio_performance.html - Portfolio Performance Chart")
        print("  • charts/matplotlib_candlestick.png - Matplotlib Candlestick Chart")
        print("  • charts/matplotlib_technical.png - Matplotlib Technical Indicators Chart")
        
    except Exception as e:
        print(f"❌ Error occurred during demo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())