from domain.repositories.stock_repository import StocksRepository
from domain.models.stock import AggregatedStockData
import pandas as pd


class DatabaseManager:
    def __init__(self, repository: StocksRepository, session):
        self.repository = repository
        self.session = session

    def fetch_and_store_data(self, ticker, start_date, end_date, granularity):
        stock_data = self.repository.get_stock_data(
            ticker, start_date, end_date, granularity
        )
        self.store_aggregated_data(stock_data)

    def store_aggregated_data(self, stock_data):
        for record in stock_data:
            aggregated_record = AggregatedStockData(
                ticker=record["ticker"], date=record["date"], price=record["price"]
            )
            self.session.add(aggregated_record)
        self.session.commit()

    def store_stock_data_from_csv(self, csv_file):
        stock_data = pd.read_csv(csv_file)
        for _, record in stock_data.iterrows():
            aggregated_record = AggregatedStockData(
                ticker=record["ticker"], date=record["date"], price=record["price"]
            )
            self.session.add(aggregated_record)
        self.session.commit()
        print(f"Data from {csv_file} successfully inserted into the database.")
