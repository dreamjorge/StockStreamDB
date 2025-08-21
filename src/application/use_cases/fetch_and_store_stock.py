# src/application/use_cases/fetch_and_store_stock.py

from src.domain.models.stock import Stock
from src.domain.repositories.stock_repository import StockRepository
from src.infrastructure.fetchers.stock_fetcher import StockFetcher
from datetime import datetime


class FetchAndStoreStockUseCase:
    def __init__(self, stock_fetcher: StockFetcher, stock_repository: StockRepository):
        self.stock_fetcher = stock_fetcher
        self.stock_repository = stock_repository

    def execute(self, ticker, period):
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
