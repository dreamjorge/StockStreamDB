from src.domain.models.stock import Stock
from src.infrastructure.db.stock_repository import StockRepository

class CollectStockData:
    def __init__(self, stock_repository):
        self.stock_repository = stock_repository

    def execute(self, ticker: str, period: str):
        # Get the stock data
        stock_data = self.stock_repository.get_stock_data(ticker, period)

        # Handle the case where no data is found
        if stock_data is None:
            print(f"No data found for {ticker} in the period '{period}'.")
            return None

        # Create the Stock entity with the correct parameters
        stock = Stock(ticker, stock_data['name'], stock_data['sector'], stock_data['close'])

        return stock
