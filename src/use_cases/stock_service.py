from src.domain.repositories.stock_repository import StockRepository
from src.domain.models.stock import Stock
from src.infrastructure.fetchers.stock_fetcher import StockFetcher
from datetime import datetime


class StockService:
    """Service for managing stock data."""

    def __init__(self, stock_repository: StockRepository, stock_fetcher: StockFetcher):
        """Initialize the service.

        Args:
            stock_repository: The stock repository.
            stock_fetcher: The stock fetcher.
        """
        self.stock_repository = stock_repository
        self.stock_fetcher = stock_fetcher

    def fetch_stock(self, ticker: str):
        """Fetches stock data for the given ticker.

        Args:
            ticker: The stock ticker.

        Returns:
            The stock data.

        Raises:
            ValueError: If the ticker is None or empty.
        """
        if ticker is None:
            raise ValueError("Ticker cannot be None")
        if ticker.strip() == "":
            raise ValueError("Ticker cannot be empty")

        stock = self.stock_repository.get_by_ticker(ticker)
        if not stock:
            stock_data = self.stock_fetcher.get_stock_data(ticker)
            if stock_data:
                stock = Stock(
                    id=None,
                    ticker=ticker,
                    name=stock_data.get("name"),
                    industry=stock_data.get("industry"),
                    sector=stock_data.get("sector"),
                    date=datetime.strptime(stock_data["date"], "%Y-%m-%d"),
                    close=stock_data["close"],
                )
                self.stock_repository.add(stock)
        return stock

    def add_stock(self, stock: Stock) -> Stock:
        """Adds a stock to the repository.

        Args:
            stock: The stock to add.

        Returns:
            The added stock.
        """
        return self.stock_repository.add(stock)

    def remove_stock(self, ticker: str) -> None:
        """Removes a stock from the repository.

        Args:
            ticker: The stock ticker.
        """
        self.stock_repository.delete(ticker)
