# src/application/use_cases/fetch_and_store_stock.py

from src.domain.models.stock import Stock
from src.domain.repositories.stock_repository import StockRepository
from src.infrastructure.fetchers.stock_fetcher import StockFetcher
from datetime import datetime


class FetchAndStoreStockUseCase:
    """Use case for fetching and storing stock data."""

    def __init__(self, stock_fetcher: StockFetcher, stock_repository: StockRepository):
        """Initialize the use case.

        Args:
            stock_fetcher: The stock fetcher.
            stock_repository: The stock repository.
        """
        self.stock_fetcher = stock_fetcher
        self.stock_repository = stock_repository

    def execute(self, ticker, period):
        """Execute the use case.

        Args:
            ticker: The stock ticker.
            period: The period to fetch the data for.
        """
        data = self.stock_fetcher.get_stock_data(ticker, period)
        if data:  # If data is not None or empty
            stock = Stock(
                id=None,
                ticker=ticker,
                name=data.get("name"),
                industry=data.get("industry"),
                sector=data.get("sector"),
                date=datetime.strptime(data["date"], "%Y-%m-%d"),
                close=data["close"],
            )
            self.stock_repository.add(stock)
