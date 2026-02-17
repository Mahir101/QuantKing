import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional
import logging

class YahooFetcher:
    """Yahoo Finance data fetcher"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def fetch_historical_data(
        self,
        symbol: str,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        interval: str = '1d'
    ) -> pd.DataFrame:
        """
        Fetch historical data
        :param symbol: Stock symbol (e.g., 'AAPL', 'MSFT')
        :param start_time: Start time
        :param end_time: End time
        :param interval: Time interval ('1d', '1wk', '1mo')
        :return: DataFrame containing OHLCV data
        """
        try:
            # Default to last year if no time specified
            if not start_time:
                start_time = datetime.now() - timedelta(days=365)
            if not end_time:
                end_time = datetime.now()

            # Fetch data
            ticker = yf.Ticker(symbol)
            df = ticker.history(
                start=start_time,
                end=end_time,
                interval=interval
            )

            # Rename columns to maintain consistency
            df.columns = [x.lower() for x in df.columns]
            
            self.logger.info(f"Successfully fetched {len(df)} records for {symbol}")
            return df

        except Exception as e:
            self.logger.error(f"Error fetching data for {symbol}: {str(e)}")
            raise

    def get_company_info(self, symbol: str) -> dict:
        """Fetch company information"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            return {
                'name': info.get('longName'),
                'sector': info.get('sector'),
                'industry': info.get('industry'),
                'market_cap': info.get('marketCap'),
                'pe_ratio': info.get('trailingPE'),
                'dividend_yield': info.get('dividendYield'),
                'beta': info.get('beta')
            }
        except Exception as e:
            self.logger.error(f"Error fetching company info for {symbol}: {str(e)}")
            raise

    def get_financial_data(self, symbol: str) -> dict:
        """Fetch financial data"""
        try:
            ticker = yf.Ticker(symbol)
            return {
                'balance_sheet': ticker.balance_sheet,
                'income_statement': ticker.financials,
                'cash_flow': ticker.cashflow
            }
        except Exception as e:
            self.logger.error(f"Error fetching financial data for {symbol}: {str(e)}")
            raise