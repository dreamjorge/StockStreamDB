import pandas as pd
from sqlalchemy.orm import Session
from src.infrastructure.db.stock_repository import StockRepository
from src.domain.models.stock import Stock
from src.interfaces.common.enums import Granularity

class ConcreteStockRepository(StockRepository):

    def __init__(self, session: Session):
        self.session = session

    def create_stock(self, stock: Stock):
        self.session.add(stock)
        self.session.commit()

    def update_stock(self, stock: Stock):
        self.session.merge(stock)
        self.session.commit()

    def delete_stock(self, ticker: str):
        stock = self.get_stock_by_ticker(ticker)
        if stock:
            self.session.delete(stock)
            self.session.commit()

    def get_stock_by_ticker(self, ticker: str, granularity: Granularity = Granularity.DAILY) -> Stock:
        query = self.session.query(Stock).filter(Stock.ticker == ticker).all()

        # Convert query results to DataFrame for aggregation
        data = [{'date': result.date, 'price': result.close_price} for result in query]
        df = pd.DataFrame(data)

        # Resample data based on the specified granularity
        df['date'] = pd.to_datetime(df['date'])
        resampled_data = df.resample(granularity.resample_rule(), on='date').agg({'price': 'mean'}).reset_index()

        # Assuming the result is a single Stock object (customize as per your need)
        return Stock(
            ticker=ticker,
            name='Aggregated Stock',
            industry='N/A',  # Fill these values as appropriate
            sector='N/A',
            close_price=resampled_data['price'].iloc[-1],  # Take the last value as the latest
            date=resampled_data['date'].iloc[-1]
        )
