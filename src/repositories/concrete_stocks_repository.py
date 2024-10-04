import pandas as pd
from src.repositories.stock_repository import StockRepository
from src.interfaces.common.enums import Granularity
from sqlalchemy import func
from src.domain.models.stock import Stock  # Stock is your model

class ConcreteStocksRepository(StockRepository):
    def __init__(self, session):
        self.session = session

    def get_stock_data(self, ticker, start_date, end_date, granularity=Granularity.DAILY):
        # Fetch stock data from the database
        query = self.session.query(Stock).filter(
            Stock.ticker == ticker,
            Stock.date >= start_date,
            Stock.date <= end_date
        ).all()

        # Convert query results to DataFrame for aggregation
        data = [{'date': result.date, 'price': result.close} for result in query]  # Ensure 'close' is used correctly
        df = pd.DataFrame(data)

        # Check if the DataFrame is empty
        if df.empty:
            raise ValueError(f"No data found for ticker {ticker} between {start_date} and {end_date}.")

        # Resample data based on the desired granularity
        df['date'] = pd.to_datetime(df['date'])
        return df.resample(granularity.resample_rule(), on='date').agg({'price': 'mean'}).reset_index()


    def create_stock(self, stock: Stock):
        self.session.add(stock)
        self.session.commit()

    def delete_stock(self, ticker: str):
        stock = self.session.query(Stock).filter(Stock.ticker == ticker).first()
        if stock:
            self.session.delete(stock)
            self.session.commit()

    def get(self, ticker: str) -> Stock:
        return self.session.query(Stock).filter(Stock.ticker == ticker).first()

    def save(self, stock: Stock):
        self.session.add(stock)
        self.session.commit()

    def update(self, stock: Stock):
        self.session.merge(stock)
        self.session.commit()
