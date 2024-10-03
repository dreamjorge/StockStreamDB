# src/application/use_cases/manage_stock.py

from domain.models.stock import Stock
from datetime import datetime

from domain.models.stock import Stock
from datetime import datetime


class ManageStockUseCase:
    def __init__(self, stock_repo, stock_fetcher=None):
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
        self.stock_repo.add(stock)  # Use consistent add method
        self.stock_repo.commit()  # Commit the session after adding the stock

    def fetch_stock_data(self, ticker, period):
        """Fetch stock data using the stock fetcher and save it to the repository."""
        data = self.stock_fetcher.fetch(ticker, period)

        # Convert date strings to datetime objects
        for stock_record in data:
            if isinstance(stock_record['date'], str):
                stock_record['date'] = datetime.strptime(stock_record['date'], '%Y-%m-%d').date()

        for stock_record in data:
            # Create a Stock instance for each record
            stock = Stock(
                ticker=stock_record['ticker'],
                name=None,  # If available, add a proper name
                industry=None,  # Add industry if available
                sector=None,  # Add sector if available
                date=stock_record['date'],
                open=stock_record['open'],
                high=stock_record['high'],
                low=stock_record['low'],
                close=stock_record['close'],
                volume=stock_record['volume']
            )
            
            # Debugging line to check stock data before insertion
            print(f"Adding stock: {stock.__dict__}")  # Check that id is not manually set
            
            self.stock_repo.add(stock)  # Add the stock object
        
        self.stock_repo.commit()  # Ensure that the data is committed to the session


    def delete_stock(self, ticker):
        """Delete a stock by its ticker."""
        stock = self.stock_repo.get_by_ticker(ticker)
        if stock:
            self.stock_repo.delete(stock)  # Ensure this calls delete on the repository
            return True
        return False

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

        self.stock_repo.update(stock)  # Ensure stock is updated
        return stock

    def check_stock_exists(self, ticker, period):
        """Check if stock data for the ticker and period already exists."""
        return self.stock_repo.stock_exists(ticker, period)
