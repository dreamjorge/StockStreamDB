from abc import ABC, abstractmethod


class StockFetcher(ABC):
    """Abstract base class for stock fetchers."""

    @abstractmethod
    def get_stock_data(self, ticker: str, period: str):
        """Fetch stock data for the given ticker and period.

        Args:
            ticker: The stock ticker.
            period: The period to fetch the data for.
        """