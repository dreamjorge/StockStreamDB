from repositories.stock_repository import StockRepository
from domain.models.stock import Stock
from infrastructure.fetchers.stock_fetcher import StockFetcher


class StockService:
    def __init__(self, stock_repository: StockRepository, stock_fetcher: StockFetcher):
        self.stock_repository = stock_repository
        self.stock_fetcher = stock_fetcher

    def _validate_ticker(self, ticker: str):
        """Helper method to validate ticker."""
        if not ticker or ticker.strip() == "":
            raise ValueError("Ticker cannot be None or empty")

    def _create_stock_from_data(self, stock_data: dict) -> Stock:
        """Helper method to create a Stock instance from data dictionary."""
        return Stock(
            ticker=stock_data["ticker"],
            name=stock_data["name"],
            industry=stock_data["industry"],
            sector=stock_data["sector"],
            close=stock_data["close"],
            date=stock_data["date"],
        )

    def fetch_stock(self, ticker: str) -> Stock:
        self._validate_ticker(ticker)
        stock = self.stock_repository.get_stock(ticker)

        if not stock:
            stock_data = self.stock_fetcher.fetch(ticker)
            stock = self._create_stock_from_data(stock_data)
            self.stock_repository.create_stock(stock)

        return stock

    def add_stock(self, stock: Stock) -> bool:
        return self.stock_repository.create_stock(stock)

    def remove_stock(self, ticker: str) -> bool:
        self._validate_ticker(ticker)
        return self.stock_repository.delete_stock(ticker)

    def get_price_alert(self, stock: Stock) -> str:
        if stock.close > 500:
            return f"Alert: The price of {stock.ticker} has exceeded $500."
        return None
