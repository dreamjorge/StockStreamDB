# src/application/use_cases/fetch_and_store_stock_use_case.py

from domain.models.stock import Stock

class FetchAndStoreStockUseCase:
    def __init__(self, yahoo_finance_fetcher, stock_repository):
        self.yahoo_finance_fetcher = yahoo_finance_fetcher
        self.stock_repository = stock_repository

    def execute(self, ticker, period):
        data = self.yahoo_finance_fetcher.fetch(ticker, period)
        if data:  # If data is not None or empty
            stock = Stock(
                ticker=data['ticker'],
                name="Unknown",  # Update according to your needs
                industry="Unknown",
                sector="Unknown",
                close_price=data['close_price'],
                date=data['date'],
                open=data['open'],
                high=data['high'],
                low=data['low'],
                volume=data['volume']
            )
            self.stock_repository.create_stock(stock)
