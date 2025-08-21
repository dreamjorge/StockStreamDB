# application/use_cases/manage_stock.py

from src.domain.repositories.stock_repository import StockRepository
from src.infrastructure.fetchers.stock_fetcher import StockFetcher


class ManageStockUseCase:
    def __init__(
        self, stock_repo: StockRepository, stock_fetcher: StockFetcher = None
    ):
        self.stock_repo = stock_repo
        self.stock_fetcher = stock_fetcher