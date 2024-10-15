from repositories.stock_repository import StockRepository
from domain.models.stock import Stock
from infrastructure.fetchers.stock_fetcher import StockFetcher


class StockService:
    def __init__(self, stock_repository: StockRepository, stock_fetcher: StockFetcher):
        self.stock_repository = stock_repository
        self.stock_fetcher = stock_fetcher

    def fetch_stock(self, ticker: str):
        if ticker is None:
            raise ValueError("Ticker cannot be None")
        if ticker.strip() == "":
            raise ValueError("Ticker cannot be empty")

        stock = self.stock_repository.get_stock(ticker)
        if not stock:
            stock_data = self.stock_fetcher.fetch(ticker)
            stock = Stock(
                ticker=stock_data["ticker"],
                name=stock_data["name"],
                industry=stock_data["industry"],
                sector=stock_data["sector"],
                close=stock_data["close"],
                date=stock_data["date"],
            )
            self.stock_repository.create_stock(stock)
        return stock

    def add_stock(self, stock: Stock) -> bool:
        return self.stock_repository.create_stock(stock)

    def remove_stock(self, ticker: str) -> bool:
        return self.stock_repository.delete_stock(ticker)

    def get_price_alert(self, stock):
        if stock.close > 500:
            return f"Alerta: El precio de {stock.ticker} ha superado los $500."
        return None
