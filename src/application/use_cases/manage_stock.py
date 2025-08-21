# application/use_cases/manage_stock.py

from src.domain.repositories.stock_repository import StockRepository
from src.infrastructure.fetchers.stock_fetcher import StockFetcher


class ManageStockUseCase:
    """Use case for managing stocks."""

    def __init__(self, stock_repo: StockRepository, stock_fetcher: StockFetcher = None):
        """Initialize the use case.

        Args:
            stock_repo: The stock repository.
            stock_fetcher: The stock fetcher.
        """
        self.stock_repo = stock_repo
        self.stock_fetcher = stock_fetcher
