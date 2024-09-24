from sqlalchemy.orm import Session
from src.domain.models.stock import Stock
from src.domain.repositories.stock_repository import StockRepository

class StockRepositoryImpl(StockRepository):
    def __init__(self, session: Session):
        self.session = session

    def create_stock(self, stock: Stock) -> Stock:
        self.session.add(stock)
        self.session.commit()
        return stock

    def get_stock_by_ticker(self, ticker: str) -> Stock:
        return self.session.query(Stock).filter_by(ticker=ticker).first()

    def update_stock(self, stock: Stock) -> Stock:
        existing_stock = self.get_stock_by_ticker(stock.ticker)
        if existing_stock:
            existing_stock.name = stock.name
            existing_stock.industry = stock.industry
            existing_stock.sector = stock.sector
            self.session.commit()
            return existing_stock
        return None

    def delete_stock(self, ticker: str) -> bool:
        stock = self.get_stock_by_ticker(ticker)
        if stock:
            self.session.delete(stock)
            self.session.commit()
            return True
        return False
