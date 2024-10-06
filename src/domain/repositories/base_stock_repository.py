# src/domain/repositories/base_stock_repository.py


class BaseStockRepository:
    def create_stock(self, stock):
        raise NotImplementedError("create_stock must be implemented by subclasses")

    def get_stock_by_ticker(self, ticker):
        raise NotImplementedError(
            "get_stock_by_ticker must be implemented by subclasses"
        )

    def update_stock(self, stock):
        raise NotImplementedError("update_stock must be implemented by subclasses")

    def delete_stock(self, stock):
        raise NotImplementedError("delete_stock must be implemented by subclasses")
