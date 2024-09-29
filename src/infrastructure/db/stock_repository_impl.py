# src/infrastructure/db/stock_repository_impl.py

from src.domain.models.stock import Stock
from src.infrastructure.db.stock_repository import StockRepository
from src.infrastructure.db.db_setup import SessionLocal  # Assuming you have a SessionLocal configured

class StockRepositoryImpl(StockRepository):
    def __init__(self, session=None):
        self.session = session or SessionLocal()

    def create_stock(self, stock):
        self.session.add(stock)
        self.session.commit()

    def get_stock_by_ticker(self, ticker: str) -> Stock:
        # Implementation for fetching a stock by its ticker
        pass

    def update_stock(self, stock: Stock):
        # Implementation for updating a stock in the database
        pass

    def delete_stock(self, ticker):
        stock = self.session.query(Stock).filter_by(ticker=ticker).first()  # Corrected: self.session
        if stock:
            self.session.delete(stock)
            self.session.commit()
            return True
        return False
    
    def get(self, ticker: str) -> Stock:
        # Fetch stock by ticker
        return self.session.query(Stock).filter(Stock.ticker == ticker).first()

    def save(self, stock: Stock):
            self.session.add(stock)
            self.session.commit()
            
    def update(self, stock: Stock) -> Stock:
        # Use session.merge() to update the stock record
        self.session.merge(stock)
        self.session.commit()
        return stock