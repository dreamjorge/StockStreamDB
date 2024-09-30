# src/repositories/stock_fetcher.py

from abc import ABC, abstractmethod

class StockFetcher(ABC):

    @abstractmethod
    def fetch(self, ticker: str, period: str):
        """Fetch stock data from an external source."""
        pass
