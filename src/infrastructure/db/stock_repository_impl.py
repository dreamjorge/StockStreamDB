from sqlalchemy.orm import Session
from src.domain.models.stock import Stock
from src.repositories.stock_repository import StockRepository
from datetime import datetime
from typing import List
from sqlalchemy.exc import SQLAlchemyError

class StockRepositoryImpl(StockRepository):
    def __init__(self, session: Session):
        self.session = session

    def get(self, ticker: str) -> Stock:
        return self.session.query(Stock).filter_by(ticker=ticker).first()

    def create(self, stock: Stock) -> None:
        try:
            self.session.add(stock)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e

    def update(self, stock: Stock) -> Stock:
        existing_stock = self.get(stock.ticker)
        if existing_stock:
            self.session.merge(stock)
            self.session.commit()
            return stock
        return None

    def delete(self, ticker: str) -> bool:
        stock = self.get_stock_by_ticker(ticker)
        if stock:
            self.session.delete(stock)
            self.session.commit()
            return True
        return False

    def get_stock_data(self, ticker: str, start: datetime, end: datetime, granularity: str) -> List[Stock]:
        query = self.session.query(Stock).filter(
            Stock.ticker == ticker,
            Stock.date >= start,
            Stock.date <= end
        )
        
        if granularity == 'monthly':
            query = query.group_by(func.date_trunc('month', Stock.date))
        
        return query.all()
        
    def create_stock(self, stock: Stock) -> None:
        """Implementing the abstract method create_stock"""
        self.create(stock)

    def delete_stock(self, ticker: str) -> bool:
        stock = self.get_stock_by_ticker(ticker)
        if stock:
            self.session.delete(stock)
            self.session.commit()
            return True
        return False

    def save(self, stock: Stock) -> Stock:
        """Implementing the abstract method save"""
        existing_stock = self.get(stock.ticker)
        if existing_stock:
            return self.update(stock)
        else:
            self.create(stock)
            return stock

    def get_stock_by_ticker(self, ticker: str) -> Stock:
        """Fetch stock by ticker from the database"""
        return self.session.query(Stock).filter_by(ticker=ticker).first()
