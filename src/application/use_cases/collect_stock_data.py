# src/application/use_cases/collect_stock_data.py


class CollectStockData:
    """Use case for collecting stock data."""

    def __init__(self, stock_fetcher_service):
        """Initialize the use case.

        Args:
            stock_fetcher_service: The stock fetcher service.
        """
        self.stock_fetcher_service = stock_fetcher_service

    def execute(self, ticker, period="1mo"):
        """Execute the use case.

        Args:
            ticker: The stock ticker.
            period: The period to fetch the data for.

        Returns:
            The stock data.
        """
        valid_periods = ["1mo", "3mo", "6mo", "1y", "5y"]
        stock_data = self.stock_fetcher_service.fetch(ticker)

        if stock_data is None:
            print(f"No data found for {ticker}.")
            return None

        if period not in valid_periods:
            raise ValueError("Invalid period")
        return stock_data
