from data_service.fetchers import BinanceFetcher
import pandas as pd
pd.set_option('display.max_rows', 10)

def main():
    # Initialize fetcher (API key not required)
    fetcher = BinanceFetcher()
    
    try:
        # Fetch current BTC price
        btc_price = fetcher.get_current_price("BTCUSD")
        print(f"\nBTC Current Price: ${btc_price:,.2f}")
        
        # Fetch historical K-line data
        df = fetcher.fetch_historical_data(
            symbol="BTCUSD",
            interval="1h"  # 1 hour K-line
        )
        print("\nLast 5 rows of historical data:")
        print(df.tail())
        
        # Fetch market depth
        depth = fetcher.get_market_depth("BTCUSD", limit=5)
        print("\nMarket Depth:")
        print("Bids:", depth['bids'])
        print("Asks:", depth['asks'])
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()