# src/use_cases/stock_service.py
from src.repositories.stock_repository import StockRepository
from src.domain.models.stock import Stock

class StockService:
    def __init__(self, repository: StockRepository):
        self.repository = repository

    def fetch_stock(self, ticker: str) -> Stock:
        return self.repository.get_stock(ticker)

    def add_stock(self, stock: Stock) -> bool:
        return self.repository.create_stock(stock)

    def remove_stock(self, ticker: str) -> bool:
        return self.repository.delete_stock(ticker)
