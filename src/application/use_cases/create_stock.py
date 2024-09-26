class CreateStock:
    def __init__(self, stock_repository):
        self.stock_repository = stock_repository
    
    def execute(self, stock):
        return self.stock_repository.create_stock(stock)
