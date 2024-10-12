# src/application/use_cases/collect_stock_data.py


class CollectStockData:
    def __init__(self, stock_fetcher_service):
        self.stock_fetcher_service = stock_fetcher_service

    def execute(self, ticker, period="1mo"):
        valid_periods = ["1mo", "3mo", "6mo", "1y", "5y"]
        stock_data = self.stock_fetcher_service.fetch(ticker)

        if stock_data is None:
            print(f"No data found for {ticker}.")
            return None

        if period not in valid_periods:
            raise ValueError("Invalid period")
        return stock_data
