from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.models.stock import Stock


class StockRepository(ABC):
    """Abstract base class for stock repositories."""

    @abstractmethod
    def add(self, stock: Stock) -> Stock:
        """Add a stock to the repository.

        Args:
            stock: The stock to add.

        Returns:
            The added stock.
        """
        pass

    @abstractmethod
    def get_by_ticker(self, ticker: str) -> Optional[Stock]:
        """Get a stock by its ticker.

        Args:
            ticker: The stock ticker.

        Returns:
            The stock if found, otherwise None.
        """
        pass

    @abstractmethod
    def get_all(self) -> List[Stock]:
        """Get all stocks from the repository.

        Returns:
            A list of all stocks.
        """
        pass

    @abstractmethod
    def update(self, stock: Stock) -> Stock:
        """Update a stock in the repository.

        Args:
            stock: The stock to update.

        Returns:
            The updated stock.
        """
        pass

    @abstractmethod
    def delete(self, ticker: str) -> None:
        """Delete a stock from the repository.

        Args:
            ticker: The stock ticker.
        """
        pass
