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

    def get(self, ticker: str) -> Stock:
        return self.session.query(Stock).filter_by(ticker=ticker).first()

    def update(self, stock: Stock) -> Stock:
        existing_stock = self.get(stock.ticker)
        if existing_stock:
            print(f"Updating stock: {existing_stock.ticker}")
            # Dynamically update all fields from the incoming stock object
            for attr, value in stock.__dict__.items():
                if hasattr(existing_stock, attr) and attr != "_sa_instance_state":
                    print(f"Updating {attr}: {getattr(existing_stock, attr)} -> {value}")
                    setattr(existing_stock, attr, value)
            
            self.session.commit()
            return existing_stock
        print("Stock not found")
        return None


    def delete_stock(self, ticker: str) -> bool:
        stock = self.get(ticker)
        if stock:
            self.session.delete(stock)
            self.session.commit()
            return True
        return False
