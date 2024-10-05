# src/use_cases/stock_service.py
from src.repositories.stock_repository import StockRepository
from src.domain.models.stock import Stock
from src.infrastructure.fetchers.stock_fetcher import StockFetcher

class StockService:
    def __init__(self, stock_repository: StockRepository, stock_fetcher: StockFetcher):
        self.stock_repository = stock_repository
        self.stock_fetcher = stock_fetcher

    def fetch_stock(self, ticker: str):
        stock = self.stock_repository.get_stock(ticker)
        if not stock:
            stock_data = self.stock_fetcher.fetch(ticker)
            stock = Stock(
                ticker=stock_data['ticker'],
                name=stock_data['name'],
                industry=stock_data['industry'],
                sector=stock_data['sector'],
                close=stock_data['close'],
                date=stock_data['date']
            )
            self.stock_repository.create_stock(stock)
        return stock
