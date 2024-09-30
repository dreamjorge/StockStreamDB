# src/repositories/stock_repository.py
from abc import ABC, abstractmethod
from src.domain.models.stock import Stock
from datetime import datetime
from src.interfaces.common.enums import Granularity
from typing import List

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
    def get_stock_data(self, ticker: str, start_date: datetime, end_date: datetime, granularity: Granularity)-> List[Stock]:
        """Retrieve stock data for a given period with a specified granularity."""
        pass
