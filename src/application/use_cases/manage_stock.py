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
        return self.stock_repository.get(ticker)

class UpdateStock:
    def __init__(self, stock_repository):
        self.stock_repository = stock_repository

    def execute(self, stock):
        # Fetch the existing stock record from the repository
        existing_stock = self.stock_repository.get(stock.ticker)

        # Update fields dynamically
        for attr, value in stock.__dict__.items():
            if hasattr(existing_stock, attr):
                setattr(existing_stock, attr, value)

        # Save updated stock back to the repository
        self.stock_repository.update(existing_stock)

        return existing_stock


class DeleteStock:
    def __init__(self, stock_repository: StockRepository):
        self.stock_repository = stock_repository

    def execute(self, ticker: str) -> bool:
        return self.stock_repository.delete_stock(ticker)
