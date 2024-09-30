# src/application/use_cases/manage_stock.py

from domain.models.stock import Stock


class ManageStockUseCase:
    def __init__(self, stock_repository):
        self.stock_repository = stock_repository

    def create_stock(self, ticker, name, industry, sector, close_price, date):
        stock = Stock(ticker=ticker, name=name, industry=industry, sector=sector, close_price=close_price, date=date)
        self.stock_repository.create_stock(stock)  # Call the repository to save it
        return stock  # Return the created stock object

    def fetch_stock_data(self, ticker, period):
        # Implementation to fetch stock data
        pass
    
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
        
        # Update fields if provided
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
