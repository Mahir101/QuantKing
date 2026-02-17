from binance.client import Client
from binance.websockets import BinanceSocketManager
from datetime import datetime
import pandas as pd
import logging
from typing import Optional, Dict, Any, Callable
import asyncio
from ..utils.exceptions import DataFetchError

class BinanceFetcher:
    """Binance context data fetcher"""
    
    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None):
        """
        Initialize Binance client
        :param api_key: Binance API key (optional)
        :param api_secret: Binance API secret (optional)
        """
        self.logger = logging.getLogger(__name__)
        try:
            self.client = Client(api_key, api_secret, tld='us')
            self.bm = None  # WebSocket manager
            self.ws_connections = {}  # Store WebSocket connections
            self.logger.info("Binance fetcher initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize Binance client: {str(e)}")
            raise

    def fetch_historical_data(
        self,
        symbol: str = "BTCUSD",
        interval: str = "1h",
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: int = 1000
    ) -> pd.DataFrame:
        """
        Fetch historical K-line data
        :param symbol: Trading pair
        :param interval: K-line interval
        :param start_time: Start time
        :param end_time: End time
        :param limit: Number of K-lines to return
        :return: DataFrame containing OHLCV data
        """
        try:
            # Convert time format
            start_str = int(start_time.timestamp() * 1000) if start_time else None
            end_str = int(end_time.timestamp() * 1000) if end_time else None
            
            # Fetch K-line data
            klines = self.client.get_klines(
                symbol=symbol,
                interval=interval,
                startTime=start_str,
                endTime=end_str,
                limit=limit
            )
            
            # Convert to DataFrame
            df = pd.DataFrame(klines, columns=[
                'timestamp', 'open', 'high', 'low', 'close', 'volume',
                'close_time', 'quote_volume', 'trades', 'taker_buy_base',
                'taker_buy_quote', 'ignore'
            ])
            
            # Process data types
            numeric_columns = ['open', 'high', 'low', 'close', 'volume']
            df[numeric_columns] = df[numeric_columns].astype(float)
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            
            self.logger.info(f"Successfully fetched {len(df)} records for {symbol}")
            return df
            
        except Exception as e:
            self.logger.error(f"Error fetching historical data: {str(e)}")
            raise DataFetchError(f"Failed to fetch historical data: {str(e)}")

    async def start_websocket(self, symbol: str, callback: Callable[[Dict], None]):
        """
        Start WebSocket real-time data stream
        :param symbol: Trading pair
        :param callback: Callback function to process real-time data
        """
        try:
            if not self.bm:
                self.bm = BinanceSocketManager(self.client)
            
            # Create K-line data connection
            conn_key = f"{symbol.lower()}@kline_1m"
            
            def handle_socket_message(msg):
                try:
                    if msg['e'] == 'kline':
                        data = {
                            'symbol': msg['s'],
                            'timestamp': pd.to_datetime(msg['E'], unit='ms'),
                            'open': float(msg['k']['o']),
                            'high': float(msg['k']['h']),
                            'low': float(msg['k']['l']),
                            'close': float(msg['k']['c']),
                            'volume': float(msg['k']['v'])
                        }
                        callback(data)
                except Exception as e:
                    self.logger.error(f"Error processing websocket message: {str(e)}")
            
            self.ws_connections[conn_key] = self.bm.start_kline_socket(
                symbol=symbol,
                callback=handle_socket_message,
                interval='1m'
            )
            
            # Start WebSocket
            self.bm.start()
            self.logger.info(f"WebSocket started for {symbol}")
            
        except Exception as e:
            self.logger.error(f"Error starting websocket: {str(e)}")
            raise

    def stop_websocket(self, symbol: str):
        """Stop WebSocket connection"""
        try:
            conn_key = f"{symbol.lower()}@kline_1m"
            if conn_key in self.ws_connections:
                self.bm.stop_socket(self.ws_connections[conn_key])
                del self.ws_connections[conn_key]
                self.logger.info(f"WebSocket stopped for {symbol}")
        except Exception as e:
            self.logger.error(f"Error stopping websocket: {str(e)}")
            raise

    def get_order_book(self, symbol: str = "BTCUSD", limit: int = 100) -> Dict:
        """
        Fetch order book data
        :param symbol: Trading pair
        :param limit: Order book depth
        :return: Order book data
        """
        try:
            depth = self.client.get_order_book(symbol=symbol, limit=limit)
            return {
                'bids': [[float(price), float(qty)] for price, qty in depth['bids']],
                'asks': [[float(price), float(qty)] for price, qty in depth['asks']]
            }
        except Exception as e:
            self.logger.error(f"Error fetching order book: {str(e)}")
            raise DataFetchError(f"Failed to fetch order book: {str(e)}")

    def get_recent_trades(self, symbol: str = "BTCUSD", limit: int = 100) -> pd.DataFrame:
        """
        Fetch recent trades
        :param symbol: Trading pair
        :param limit: Number of recent trades to return
        :return: Recent trades data
        """
        try:
            trades = self.client.get_recent_trades(symbol=symbol, limit=limit)
            df = pd.DataFrame(trades)
            df['time'] = pd.to_datetime(df['time'], unit='ms')
            df['price'] = df['price'].astype(float)
            df['qty'] = df['qty'].astype(float)
            return df
        except Exception as e:
            self.logger.error(f"Error fetching recent trades: {str(e)}")
            raise DataFetchError(f"Failed to fetch recent trades: {str(e)}")