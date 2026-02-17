from data_service import BinanceFetcher, DataProcessor
import pandas as pd
from data_service.utils.logger import setup_logger

def main():
    # Setup logging
    logger = setup_logger("crypto_data")
    
    try:
        # 1. Initialize Binance data fetcher
        fetcher = BinanceFetcher()
        
        # 2. Initialize data processor
        processor = DataProcessor()
        
        # 3. Fetch BTC data
        logger.info("Fetching BTC data...")
        
        # Get current price
        btc_price = fetcher.get_current_price("BTCUSD")
        print(f"\nBTC Current Price: ${btc_price:,.2f}")
        
        # Fetch historical K-line data
        df = fetcher.fetch_historical_data(
            symbol="BTCUSD",
            interval="1h"  # 1 hour K-line
        )
        print("\nLast 5 rows of historical data:")
        print(df.tail())
        
        # 4. Process data
        processed_data = processor.process_market_data(df)
        
        # 5. Print analysis results
        print("\n=== Market Statistics ===")
        for key, value in processed_data.statistics.items():
            print(f"{key}: {value:.4f}")
        
        print("\n=== Trading Signals ===")
        for key, value in processed_data.signals.items():
            print(f"{key}: {value}")
        
        # 6. Fetch market depth
        depth = fetcher.get_market_depth("BTCUSD", limit=5)
        print("\n=== Market Depth ===")
        print("Bids:", depth['bids'])
        print("Asks:", depth['asks'])
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()