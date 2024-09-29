from abc import ABC, abstractmethod
from src.domain.models.stock import Stock

class StockRepository(ABC):

    @abstractmethod
    def create_stock(self, stock: Stock) -> Stock:
        pass

    @abstractmethod
    def get(self, ticker: str) -> Stock:
        pass

    @abstractmethod
    def update(self, stock: Stock) -> Stock:
        pass

    @abstractmethod
    def delete_stock(self, ticker: str) -> bool:
        pass
    
    @abstractmethod
    def save(self, stock):
        pass
    
    @abstractmethod
    def get_stock_by_ticker(self, ticker: str, granularity: Granularity = Granularity.DAILY) -> Stock:
        """
        Fetch stock data by ticker with a specified granularity (daily, weekly, etc.).
        """
        pass
    
    @abstractmethod
    def get_stock_data(self, ticker, start_date, end_date, granularity=Granularity.DAILY):
        pass

