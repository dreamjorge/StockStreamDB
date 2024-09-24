from src.domain.models.stock import Stock
from src.domain.repositories.stock_repository import StockRepository

class CreateStock:
    def __init__(self, stock_repository: StockRepository):
        self.stock_repository = stock_repository

    def execute(self, stock: Stock) -> Stock:
        return self.stock_repository.create_stock(stock)

class GetStock:
    def __init__(self, stock_repository: StockRepository):
        self.stock_repository = stock_repository

    def execute(self, ticker: str) -> Stock:
        return self.stock_repository.get_stock_by_ticker(ticker)

class UpdateStock:
    def __init__(self, stock_repository: StockRepository):
        self.stock_repository = stock_repository

    def execute(self, stock: Stock) -> Stock:
        return self.stock_repository.update_stock(stock)

class DeleteStock:
    def __init__(self, stock_repository: StockRepository):
        self.stock_repository = stock_repository

    def execute(self, ticker: str) -> bool:
        return self.stock_repository.delete_stock(ticker)
