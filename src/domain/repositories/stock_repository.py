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
