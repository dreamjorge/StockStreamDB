# src/infrastructure/fetchers/stock_fetcher.py
from abc import ABC, abstractmethod


class StockFetcher(ABC):
    @abstractmethod
    def fetch(self, ticker: str):
        """Fetch stock data for a given ticker."""
