from abc import ABC, abstractmethod

class StockFetcher(ABC):
    @abstractmethod
    def get_stock_data(self, ticker: str, period: str):
        """Fetch stock data for the given ticker and period"""
        pass