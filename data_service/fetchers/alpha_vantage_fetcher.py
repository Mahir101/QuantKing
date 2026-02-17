from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.fundamentaldata import FundamentalData
import pandas as pd
import logging
from typing import Optional, Dict, Any
from datetime import datetime
from ..utils.exceptions import DataFetchError

class AlphaVantageFetcher:
    """Alpha Vantage data fetcher"""
    
    def __init__(self, api_key: str):
        """
        Initialize Alpha Vantage client
        :param api_key: Alpha Vantage API key
        """
        self.logger = logging.getLogger(__name__)
        try:
            self.ts = TimeSeries(key=api_key, output_format='pandas')
            self.fd = FundamentalData(key=api_key, output_format='pandas')
            self.logger.info("Alpha Vantage fetcher initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize Alpha Vantage client: {str(e)}")
            raise

    def fetch_historical_data(
        self,
        symbol: str,
        interval: str = 'daily',
        outputsize: str = 'compact'
    ) -> pd.DataFrame:
        """
        Fetch historical data
        :param symbol: Stock symbol
        :param interval: Time interval (intraday, daily, weekly, monthly)
        :param outputsize: Data volume (compact or full)
        :return: DataFrame containing OHLCV data
        """
        try:
            if interval == 'intraday':
                data, meta_data = self.ts.get_intraday(
                    symbol=symbol,
                    interval='60min',
                    outputsize=outputsize
                )
            elif interval == 'daily':
                data, meta_data = self.ts.get_daily(
                    symbol=symbol,
                    outputsize=outputsize
                )
            elif interval == 'weekly':
                data, meta_data = self.ts.get_weekly(symbol=symbol)
            elif interval == 'monthly':
                data, meta_data = self.ts.get_monthly(symbol=symbol)
            else:
                raise ValueError(f"Invalid interval: {interval}")
            
            # Rename columns
            data.columns = ['open', 'high', 'low', 'close', 'volume']
            
            self.logger.info(f"Successfully fetched {len(data)} records for {symbol}")
            return data
            
        except Exception as e:
            self.logger.error(f"Error fetching historical data: {str(e)}")
            raise DataFetchError(f"Failed to fetch historical data: {str(e)}")

    def get_company_overview(self, symbol: str) -> Dict[str, Any]:
        """
        Fetch company overview
        :param symbol: Stock symbol
        :return: Basic company information
        """
        try:
            overview, _ = self.fd.get_company_overview(symbol)
            return overview.to_dict()
        except Exception as e:
            self.logger.error(f"Error fetching company overview: {str(e)}")
            raise DataFetchError(f"Failed to fetch company overview: {str(e)}")

    def get_income_statement(self, symbol: str) -> pd.DataFrame:
        """
        Fetch income statement
        :param symbol: Stock symbol
        :return: Income statement data
        """
        try:
            income_stmt, _ = self.fd.get_income_statement_annual(symbol)
            return income_stmt
        except Exception as e:
            self.logger.error(f"Error fetching income statement: {str(e)}")
            raise DataFetchError(f"Failed to fetch income statement: {str(e)}")

    def get_balance_sheet(self, symbol: str) -> pd.DataFrame:
        """
        Fetch balance sheet
        :param symbol: Stock symbol
        :return: Balance sheet data
        """
        try:
            balance_sheet, _ = self.fd.get_balance_sheet_annual(symbol)
            return balance_sheet
        except Exception as e:
            self.logger.error(f"Error fetching balance sheet: {str(e)}")
            raise DataFetchError(f"Failed to fetch balance sheet: {str(e)}")

    def get_cash_flow(self, symbol: str) -> pd.DataFrame:
        """
        Fetch cash flow statement
        :param symbol: Stock symbol
        :return: Cash flow data
        """
        try:
            cash_flow, _ = self.fd.get_cash_flow_annual(symbol)
            return cash_flow
        except Exception as e:
            self.logger.error(f"Error fetching cash flow: {str(e)}")
            raise DataFetchError(f"Failed to fetch cash flow: {str(e)}")