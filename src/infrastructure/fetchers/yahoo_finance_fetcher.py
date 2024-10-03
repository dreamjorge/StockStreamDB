import yfinance as yf
import pandas as pd  # <-- Add this line to import pandas
from typing import List, Dict, Union, Optional
import logging

class YahooFinanceFetcher:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def fetch(self, ticker: str, period: str = '1mo', interval: str = '1d', return_format: str = 'list') -> Union[List[Dict], Dict[str, Dict], Optional[pd.DataFrame]]:
        try:
            stock_data = yf.Ticker(ticker).history(period=period, interval=interval)
            if stock_data.empty:
                self.logger.warning(f"No data found for ticker: {ticker}")
                return []

            if return_format == 'list':
                return self._to_list(ticker, stock_data)
            elif return_format == 'dict':
                return self._to_dict(ticker, stock_data)
            elif return_format == 'dataframe':
                return stock_data
            else:
                raise ValueError(f"Unsupported return_format: {return_format}")

        except Exception as e:
            self.logger.error(f"Failed to fetch data for {ticker}: {e}")
            return None

    def _to_list(self, ticker: str, stock_data: pd.DataFrame) -> List[Dict]:
        return [
            {
                'ticker': ticker,
                'date': index.strftime('%Y-%m-%d'),
                'close': row.get('Close', None),
                'open': row.get('Open', None),
                'high': row.get('High', None),
                'low': row.get('Low', None),
                'volume': row.get('Volume', None)
            }
            for index, row in stock_data.iterrows()
        ]

    def _to_dict(self, ticker: str, stock_data: pd.DataFrame) -> Dict[str, Dict]:
        return {
            index.strftime('%Y-%m-%d'): {
                'ticker': ticker,
                'close': row.get('Close', None),
                'open': row.get('Open', None),
                'high': row.get('High', None),
                'low': row.get('Low', None),
                'volume': row.get('Volume', None)
            }
            for index, row in stock_data.iterrows()
        }
