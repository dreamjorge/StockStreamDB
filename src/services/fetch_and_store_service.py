from infrastructure.fetchers.yahoo_finance_fetcher import YahooFinanceFetcher
from infrastructure.db.stock_repository_impl import StockRepositoryImpl
from domain.models.stock import Stock


class FetchAndStoreStockService:
    def __init__(self, fetcher: YahooFinanceFetcher, stock_repo: StockRepositoryImpl):
        self.fetcher = fetcher
        self.stock_repo = stock_repo

    def fetch_and_store(self, ticker: str, period: str):
        stock_data = self.fetcher.fetch(ticker, period)
        if stock_data:
            for stock in stock_data:
                stock_entity = Stock(
                    ticker=stock["ticker"],
                    date=stock["date"],
                    close=stock["close"],
                    open_price=stock["open"],
                    high_price=stock["high"],
                    low_price=stock["low"],
                    volume=stock["volume"],
                )
                self.stock_repo.create(stock_entity)
            print(f"Data for {ticker} stored successfully!")
        else:
            print(f"No data found for {ticker}.")
