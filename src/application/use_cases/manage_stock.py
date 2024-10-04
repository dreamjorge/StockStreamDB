from domain.models.stock import Stock
from datetime import datetime
from datetime import timedelta
from domain.stock_fetcher import StockFetcher
from infrastructure.db.stock_repository_impl import StockRepositoryImpl

class ManageStockUseCase:
    def __init__(self, stock_repo: StockRepositoryImpl, stock_fetcher: StockFetcher):
        self.stock_repo = stock_repo
        self.stock_fetcher = stock_fetcher

    def create_stock(self, ticker, name, industry, sector, close, date):
        """Create a new stock entry."""
        stock = Stock(
            ticker=ticker,
            name=name,
            industry=industry,
            sector=sector,
            close=close,
            date=date
        )
        self.stock_repo.create_stock(stock)  # Use create_stock instead of add
        self.stock_repo.commit()
        return stock

    def fetch_and_store_stock(self, ticker: str, period: str):
        """Fetch stock data and store it in the repository."""
        stock_data = self.stock_fetcher.fetch(ticker, period)
        for stock_record in stock_data:
            stock = Stock(
                ticker=ticker,
                date=stock_record['date'],
                close=stock_record['close'],
                open=stock_record['open'],
                high=stock_record['high'],
                low=stock_record['low'],
                volume=stock_record['volume']
            )
            self.stock_repo.save(stock)
            
    def delete_stock(self, ticker):
        """Delete a stock by its ticker."""
        stock = self.stock_repo.get_by_ticker(ticker)
        if stock:
            self.stock_repo.delete(stock)  # Ensure this calls delete on the repository
            self.stock_repo.commit()  # Commit the transaction after deletion
            return True
        return False  # Return False if the stock was not found

    def update_stock(self, ticker, close=None, name=None, industry=None, sector=None):
        """Update stock details."""
        stock = self.stock_repo.get_by_ticker(ticker)  # Fetch the stock by its ticker
        if not stock:
            raise ValueError(f"Stock with ticker {ticker} not found")

        # Update stock fields if provided
        if close:
            stock.close = close
        if name:
            stock.name = name
        if industry:
            stock.industry = industry
        if sector:
            stock.sector = sector

        self.stock_repo.update(stock)  # Ensure the stock is updated
        self.stock_repo.commit()  # Commit the transaction after updating
        return stock  # Return the updated stock for validation or further use

    def check_stock_exists(self, ticker, period):
        """Check if stock data for the ticker and period already exists."""
        return self.stock_repo.stock_exists(ticker, period)
    
    def fetch_stock_data(self, ticker: str, period: str):
        return self.stock_fetcher.fetch(ticker, period)