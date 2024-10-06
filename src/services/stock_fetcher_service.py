# src/services/stock_fetcher_service.py


class StockFetcherService:
    def __init__(self, fetcher):
        self.fetcher = fetcher

    def fetch(self, ticker):
        return self.fetcher.fetch(ticker)
