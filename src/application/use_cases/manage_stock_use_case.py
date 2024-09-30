from src.domain.models.stock import Stock
from src.infrastructure.db.stock_repository_impl import StockRepositoryImpl

class ManageStockUseCase:
    def __init__(self, stock_repository: StockRepositoryImpl):
        self.stock_repository = stock_repository

    def create_stock(self, ticker, name, industry, sector, close_price, date):
        stock = Stock(ticker=ticker, name=name, industry=industry, sector=sector, close_price=close_price, date=date)
        self.stock_repository.create_stock(stock)
        return stock  # Ensure to return the created stock

    def fetch_stock_data(self, ticker, period):
        return self.stock_repository.get_stock_data(ticker, period)

    def delete_stock(self, ticker):
        stock = self.stock_repository.get_stock_by_ticker(ticker)
        if stock:
            self.stock_repository.delete(ticker)  # Ensure this calls delete
            return True
        return False

    def update_stock(self, ticker, close_price=None, name=None, industry=None, sector=None):
        stock = self.stock_repository.get_stock_by_ticker(ticker)
        if not stock:
            raise ValueError(f"Stock with ticker {ticker} not found")

        if close_price:
            stock.close_price = close_price
        if name:
            stock.name = name
        if industry:
            stock.industry = industry
        if sector:
            stock.sector = sector

        self.stock_repository.update(stock)
        return stock

    def get_stock(self, ticker):
        return self.stock_repository.get_stock_by_ticker(ticker)