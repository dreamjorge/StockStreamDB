class DeleteStock:
    def __init__(self, stock_repository):
        self.stock_repository = stock_repository

    def execute(self, ticker):
        # Get existing stock by ticker
        existing_stock = self.stock_repository.get_stock_by_ticker(ticker)

        if existing_stock:
            # Delete the stock
            self.stock_repository.session.delete(existing_stock)
            self.stock_repository.session.commit()
            return True
        else:
            return False
