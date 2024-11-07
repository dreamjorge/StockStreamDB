# application/use_cases/manage_stock.py

from domain.models.stock import Stock
from domain.stock_fetcher import StockFetcher
from infrastructure.db.stock_repository_impl import StockRepositoryImpl


class ManageStockUseCase:
    def __init__(
        self, stock_repo: StockRepositoryImpl, stock_fetcher: StockFetcher = None
    ):
        self.stock_repo = stock_repo
        self.stock_fetcher = stock_fetcher

    def create_stock(self, ticker, name, industry, sector, close, date):
        if not self.validate_stock(ticker):
            raise ValueError("Invalid stock")

        stock = Stock(
            ticker=ticker,
            name=name,
            industry=industry,
            sector=sector,
            close=close,
            date=date,
        )

        self.stock_repo.save(stock)
        self.stock_repo.commit()

        return stock

    def fetch_and_store_stock(self, ticker: str, period: str):
        """Fetch stock data and store it in the repository."""
        if not self.stock_fetcher:
            raise ValueError("StockFetcher not provided.")

        stock_data = self.stock_fetcher.fetch(ticker, period)
        for stock_record in stock_data:
            stock = Stock(
                ticker=ticker,
                date=stock_record["date"],
                close=stock_record["close"],
                open=stock_record["open"],
                high=stock_record["high"],
                low=stock_record["low"],
                volume=stock_record["volume"],
            )
            self.stock_repo.save(stock)

    def delete_stock(self, ticker):
        """Delete a stock by its ticker."""
        stock = self.stock_repo.get_by_ticker(ticker)
        if stock:
            self.stock_repo.delete(stock)
            self.stock_repo.commit()
            return True
        return False

    def update_stock(self, ticker, close=None, name=None, industry=None, sector=None):
        """Update stock details."""
        stock = self.stock_repo.get_by_ticker(ticker)
        if not stock:
            raise ValueError(f"Stock with ticker {ticker} not found")

        if close:
            stock.close = close
        if name:
            stock.name = name
        if industry:
            stock.industry = industry
        if sector:
            stock.sector = sector

        self.stock_repo.update(stock)
        self.stock_repo.commit()
        return stock

    def check_stock_exists(self, ticker, period):
        """Check if stock data for the ticker and period already exists."""
        return self.stock_repo.stock_exists(ticker, period)

    def fetch_stock_data(self, ticker: str, period: str):
        if not self.stock_fetcher:
            raise ValueError("StockFetcher not provided.")
        return self.stock_fetcher.fetch(ticker, period)

    def validate_stock(self, stock):
        # Business logic for validating stock
        return True
