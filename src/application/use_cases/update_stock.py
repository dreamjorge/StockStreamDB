class UpdateStock:
    def __init__(self, stock_repository):
        self.stock_repository = stock_repository

    def execute(self, stock):
        # Get existing stock by ticker
        existing_stock = self.stock_repository.get_stock_by_ticker(stock.ticker)
        
        if existing_stock:
            # Update the fields
            existing_stock.name = stock.name
            existing_stock.industry = stock.industry
            existing_stock.sector = stock.sector
            existing_stock.close_price = stock.close_price
            existing_stock.date = stock.date

            # Commit the changes
            self.stock_repository.session.commit()
            return existing_stock
        else:
            return None
