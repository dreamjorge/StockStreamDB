# src/infrastructure/db/concrete_stocks_repository.py
from src.domain.repositories.base_stock_repository import BaseStockRepository
from src.infrastructure.db.models import Stock  # Import the Stock model
import pandas as pd


class ConcreteStocksRepository(BaseStockRepository):
    def __init__(self, session):  # Accept session as an argument
        self.session = session  # Store it as an instance variable

    def create_stock(self, stock):
        # Use self.session for database operations
        self.session.add(stock)
        self.session.commit()

    def get_stock_by_ticker(self, ticker):
        # Use self.session for database query
        return self.session.query(Stock).filter_by(ticker=ticker).first()

    def update_stock(self, stock):
        self.session.merge(stock)
        self.session.commit()

    def get_stock_data(self, ticker, start_date, end_date, granularity):
        stock_data = (
            self.session.query(Stock)
            .filter(
                Stock.ticker == ticker, Stock.date >= start_date, Stock.date <= end_date
            )
            .all()
        )

        if not stock_data:  # If no data is found
            raise ValueError(f"No data found for ticker {ticker}")

        # Convert the result to a pandas DataFrame
        df = pd.DataFrame(
            [{"date": stock.date, "price": stock.close} for stock in stock_data]
        )

        return df

    def get(self, ticker):
        return self.session.query(Stock).filter_by(ticker=ticker).first()

    def delete_stock(self, ticker):
        stock_to_delete = self.session.query(Stock).filter_by(ticker=ticker).first()
        if stock_to_delete:
            self.session.delete(stock_to_delete)
            self.session.commit()

    def save(self, stock):
        self.session.add(stock)
        self.session.commit()

    def update(self, stock):
        self.session.merge(stock)
        self.session.commit()
