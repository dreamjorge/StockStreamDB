class GetStock:
    def __init__(self, stock_repository):
        self.stock_repository = stock_repository

    def execute(self, ticker):
        # Fetch the stock data from the repository
        stock = self.stock_repository.get_stock_by_ticker(ticker)
        return stock
