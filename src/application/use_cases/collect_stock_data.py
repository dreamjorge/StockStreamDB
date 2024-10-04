from src.domain.models.stock import Stock
from src.infrastructure.db.stock_repository import StockRepository
from src.domain.stock_fetcher import StockFetcher  # Adjust the path to where StockFetcher is implemented

class CollectStockData:
    VALID_PERIODS = ['1mo', '3mo', '6mo', '1y', '5y']

    def __init__(self, stock_fetcher):
        self.stock_fetcher = stock_fetcher

    def execute(self, ticker: str, period: str):
        if period not in self.VALID_PERIODS:
            raise ValueError("Invalid period")
        
        stock_data = self.stock_fetcher.fetch(ticker, period)
        if stock_data is None:
            print(f"No data found for {ticker} in the period '{period}'.")
            return None

        stock = Stock(
            ticker=stock_data['ticker'],
            name=stock_data['name'],
            industry=stock_data['industry'],
            sector=stock_data['sector'],
            close=stock_data['close'],
            date=stock_data['date']
        )
        return stock



