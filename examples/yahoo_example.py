import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np

class YahooDataAnalyzer:
    def __init__(self):
        self.data = {}
    
    def fetch_stock_data(self, symbols: list, period: str = '1y') -> None:
        """
        Fetch stock data
        :param symbols: List of stock symbols ['AAPL', 'MSFT', etc.]
        :param period: Time range ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
        """
        for symbol in symbols:
            try:
                print(f"\nFetching data for {symbol}...")
                ticker = yf.Ticker(symbol)
                
                # Fetch historical data
                self.data[symbol] = {
                    'history': ticker.history(period=period),
                    'info': ticker.info,
                    'financials': ticker.financials,
                    'balance_sheet': ticker.balance_sheet,
                    'cashflow': ticker.cashflow
                }
                print(f"Successfully fetched data for {symbol}")
                
            except Exception as e:
                print(f"Error fetching data for {symbol}: {str(e)}")

    def analyze_stock(self, symbol: str) -> None:
        """Analyze individual stock"""
        if symbol not in self.data:
            print(f"Data not found for {symbol}")
            return
        
        stock_data = self.data[symbol]
        history = stock_data['history']
        info = stock_data['info']
        
        print(f"\n=== {symbol} Analysis Report ===")
        
        # 1. Basic Information
        print("\nBasic Information:")
        print(f"Company Name: {info.get('longName', 'N/A')}")
        print(f"Industry: {info.get('industry', 'N/A')}")
        print(f"Market Cap: ${info.get('marketCap', 0)/1e9:.2f}B")
        print(f"PE Ratio: {info.get('trailingPE', 'N/A')}")
        print(f"52-Week High: ${info.get('fiftyTwoWeekHigh', 'N/A')}")
        print(f"52-Week Low: ${info.get('fiftyTwoWeekLow', 'N/A')}")
        
        # 2. Technical Indicators
        # Calculate moving averages
        history['MA20'] = history['Close'].rolling(window=20).mean()
        history['MA50'] = history['Close'].rolling(window=50).mean()
        
        # Calculate RSI
        delta = history['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        history['RSI'] = 100 - (100 / (1 + rs))
        
        print("\nTechnical Indicators (Latest):")
        print(f"Closing Price: ${history['Close'][-1]:.2f}")
        print(f"20-day MA: ${history['MA20'][-1]:.2f}")
        print(f"50-day MA: ${history['MA50'][-1]:.2f}")
        print(f"RSI: {history['RSI'][-1]:.2f}")
        
        # 3. Plot Chart
        plt.figure(figsize=(15, 10))
        
        # Price and MAs
        plt.subplot(2, 1, 1)
        plt.plot(history.index, history['Close'], label='Price')
        plt.plot(history.index, history['MA20'], label='MA20')
        plt.plot(history.index, history['MA50'], label='MA50')
        plt.title(f'{symbol} Price Trend')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.grid(True)
        
        # Volume
        plt.subplot(2, 1, 2)
        plt.bar(history.index, history['Volume'])
        plt.title('Volume')
        plt.xlabel('Date')
        plt.ylabel('Volume')
        plt.grid(True)
        
        plt.tight_layout()
        plt.show()

def main():
    # Set stocks to analyze
    symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
    
    # Create analyzer instance
    analyzer = YahooDataAnalyzer()
    
    # Fetch data
    analyzer.fetch_stock_data(symbols)
    
    # Analyze each stock
    for symbol in symbols:
        analyzer.analyze_stock(symbol)
        
        # Wait for user input
        input("\nPress Enter to continue to next analysis...")

if __name__ == "__main__":
    # Set pandas display options
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.float_format', lambda x: '%.2f' % x)
    
    main()