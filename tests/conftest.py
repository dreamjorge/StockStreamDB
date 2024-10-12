import sys
import os
import pytest
from unittest.mock import MagicMock
from src.infrastructure.db.stock_repository_impl import StockRepositoryImpl
from src.infrastructure.fetchers.yahoo_finance_fetcher import YahooFinanceFetcher

# Ensure src is added to the system path
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)


@pytest.fixture
def mock_db_session():
    return MagicMock()


@pytest.fixture
def stock_repo(mock_db_session):
    return StockRepositoryImpl(mock_db_session)


@pytest.fixture
def mock_stock():
    return {
        "ticker": "AAPL",
        "name": "Apple",
        "industry": "Technology",
        "sector": "Consumer Electronics",
        "close": 150.0,
        "date": "2023-01-01",
    }


# Add stock_fetcher fixture
@pytest.fixture
def stock_fetcher():
    return MagicMock(spec=YahooFinanceFetcher)
