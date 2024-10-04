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
        self.stock_repo.create_stock(stock)  # Use create_stock instead of add
        self.stock_repo.commit()
        return stock

    def fetch_stock_data(self, ticker, period):
        """Fetch stock data using the stock fetcher and save it to the repository."""
        data = self.stock_fetcher.fetch(ticker, period)

        if not data:
            return None  # Handle None case if no data is fetched

        # Convert date strings to datetime objects
        for stock_record in data:
            if isinstance(stock_record['date'], str):
                stock_record['date'] = datetime.strptime(stock_record['date'], '%Y-%m-%d').date()

        # Store the fetched data
        for stock_record in data:
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
            print(f"Adding stock: {stock.__dict__}")
            
            self.stock_repo.add(stock)  # Add the stock object
        
        self.stock_repo.commit()  # Commit the changes
        return data  # Return the fetched data for validation or further use

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