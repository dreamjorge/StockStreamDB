from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.models.stock import Stock


class StockRepository(ABC):
    @abstractmethod
    def add(self, stock: Stock) -> Stock:
        pass

    @abstractmethod
    def get_by_ticker(self, ticker: str) -> Optional[Stock]:
        pass

    @abstractmethod
    def get_all(self) -> List[Stock]:
        pass

    @abstractmethod
    def update(self, stock: Stock) -> Stock:
        pass

    @abstractmethod
    def delete(self, ticker: str) -> None:
        pass