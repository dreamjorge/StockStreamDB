from sqlalchemy.orm import Session
from src.domain.models.stock import Stock
from src.repositories.stock_repository import StockRepository
from datetime import datetime
from typing import List, Optional
from datetime import timedelta


class StockRepositoryImpl(StockRepository):
    def __init__(self, session: Session):
        self.session = session

    def get(self, ticker: str) -> Optional[Stock]:
        """Fetch stock by ticker from the database."""
        return self.session.query(Stock).filter_by(ticker=ticker).first()

    def create_stock(self, stock: Stock) -> None:
        """Insert a new stock record."""
        self.session.add(stock)
        self.session.commit()

    def save(self, stock: Stock) -> Stock:
        """Save or update a stock."""
        existing_stock = self.get(stock.ticker)
        if existing_stock:
            return self.update(stock)
        else:
            self.create_stock(stock)
            return stock

    def update(self, stock: Stock) -> Stock:
        """Update an existing stock."""
        existing_stock = self.get(stock.ticker)
        if existing_stock:
            self.session.merge(stock)
            self.session.commit()
            return stock
        return None

    def delete_stock(self, ticker: str) -> bool:
        """Delete a stock by ticker."""
        stock = self.get_by_ticker(ticker)
        if stock:
            self.session.delete(stock)
            self.session.commit()
            return True
        return False

    def get_stock_data(self, ticker: str, start: datetime, end: datetime, granularity: str = None) -> List[Stock]:
        query = self.session.query(Stock).filter(
            Stock.ticker == ticker,
            Stock.date >= start,
            Stock.date <= end
        )
    
        # Optional granularity-based logic
        if granularity == 'daily':
            # Add any specific logic for daily granularity here if needed
            pass
        
        return query.all()

    def get_by_ticker(self, ticker: str) -> Stock:
        """Fetch stock by ticker from the database."""
        return self.session.query(Stock).filter_by(ticker=ticker).first()

    def stock_exists(self, ticker, period):
        """Check if stock data for the given ticker and period exists."""
        start_date, end_date = self.get_date_range_for_period(period)
        query = self.session.query(Stock).filter(
            Stock.ticker == ticker,
            Stock.date >= start_date,
            Stock.date <= end_date
        )
        return self.session.query(query.exists()).scalar()

    def get_date_range_for_period(self, period):
        """Helper method to calculate the date range based on the period."""
        today = datetime.now().date()

        if period == '1y':
            start_date = today - timedelta(days=365)
        elif period == '1m':
            start_date = today - timedelta(days=30)
        elif period == '1d':
            start_date = today - timedelta(days=1)
        elif period == '1mo':
            start_date = today - timedelta(days=30)
        else:
            raise ValueError(f"Invalid period: {period}")

        return start_date, today
    
    def get_sample_stock_data(self, ticker: str):
        return self.session.query(Stock).filter_by(ticker=ticker).limit(5).all()

    def add_stock(self, stock: Stock):
        self.session.add(stock)
        self.session.commit()

    def commit(self):
        self.session.commit()

