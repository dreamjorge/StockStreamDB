# src/application/use_cases/manage_stock.py

from domain.models.stock import Stock


class ManageStockUseCase:
    def __init__(self, stock_repo, stock_fetcher=None):
        self.stock_repo = stock_repo
        self.stock_fetcher = stock_fetcher

    def create_stock(self, ticker, name, industry, sector, close_price, date):
        """Create a new stock entry."""
        stock = Stock(
            ticker=ticker,
            name=name,
            industry=industry,
            sector=sector,
            close_price=close_price,
            date=date
        )
        self.stock_repo.create(stock)

    def fetch_stock_data(self, ticker, period):
        if not self.stock_fetcher:
            raise AttributeError("Stock fetcher is not initialized.")
        # Call stock fetcher to fetch data and do other tasks
    
    def delete_stock(self, ticker):
        stock = self.stock_repository.get_by_ticker(ticker)
        if stock:
            self.stock_repository.delete_stock(ticker)  # Ensure this calls delete
            return True
        return False

    def update_stock(self, ticker, close_price=None, name=None, industry=None, sector=None):
        stock = self.stock_repository.get_by_ticker(ticker)  # Use get_by_ticker if this is the correct method
        if not stock:
            raise ValueError(f"Stock with ticker {ticker} not found")  # This should raise the ValueError

        # Proceed to update fields if provided
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


    def check_stock_exists(self, ticker, period):
        """Check if stock data for the ticker and period already exists."""
        # Assuming you store data with a `date` field, modify this query accordingly
        return self.stock_repo.stock_exists(ticker, period)