import pytest
from src.repositories.stock_fetcher import StockFetcher


# Create a simple concrete subclass of StockFetcher for testing
class ConcreteStockFetcher(StockFetcher):
    def fetch(self, ticker: str, period: str):
        return {"ticker": ticker, "period": period}


@pytest.fixture
def stock_fetcher():
    # Provide a fixture for the concrete implementation of StockFetcher
    return ConcreteStockFetcher()


def test_fetch_method(stock_fetcher):
    # Call the fetch method and verify it returns the expected data
    result = stock_fetcher.fetch("AAPL", "1mo")
    assert result == {"ticker": "AAPL", "period": "1mo"}
