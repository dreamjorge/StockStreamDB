# src/application/use_cases/manage_stock.py
from src.domain.models.stock import Stock
from src.infrastructure.db.stock_repository import StockRepository

class ManageStockUseCase:
    def __init__(self, stock_repository: StockRepository):
        self.stock_repository = stock_repository

    def create_stock(self, ticker: str, name: str, industry: str, sector: str, close_price: float, date: str) -> Stock:
        # Create a new stock
        stock = Stock(ticker=ticker, name=name, industry=industry, sector=sector, close_price=close_price, date=date)
        self.stock_repository.create_stock(stock)
        return stock

    def update_stock(self, ticker: str, name: str = None, industry: str = None, sector: str = None, close_price: float = None, date: str = None) -> Stock:
        # Find the existing stock by ticker
        stock = self.stock_repository.get_stock_by_ticker(ticker)
        if not stock:
            raise ValueError(f"Stock with ticker {ticker} not found")

        # Update stock properties
        if name:
            stock.name = name
        if industry:
            stock.industry = industry
        if sector:
            stock.sector = sector
        if close_price:
            stock.close_price = close_price
        if date:
            stock.date = date

        self.stock_repository.update_stock(stock)
        return stock

    def delete_stock(self, ticker: str) -> bool:
        # Delete stock by ticker
        stock = self.stock_repository.get_stock_by_ticker(ticker)
        if not stock:
            return False

        self.stock_repository.delete_stock(ticker)
        return True
