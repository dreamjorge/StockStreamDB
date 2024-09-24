from abc import ABC, abstractmethod
from src.domain.models.stock import Stock

class StockRepository(ABC):

    @abstractmethod
    def create_stock(self, stock: Stock) -> Stock:
        pass

    @abstractmethod
    def get_stock_by_ticker(self, ticker: str) -> Stock:
        pass

    @abstractmethod
    def update_stock(self, stock: Stock) -> Stock:
        pass

    @abstractmethod
    def delete_stock(self, ticker: str) -> bool:
        pass
