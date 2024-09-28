# tests/test_manage_stock.py
import pytest
from unittest.mock import MagicMock
from src.application.use_cases.manage_stock import ManageStockUseCase
from src.domain.models.stock import Stock

@pytest.fixture
def mock_stock_repo():
    return MagicMock()

def test_create_stock(mock_stock_repo):
    use_case = ManageStockUseCase(stock_repository=mock_stock_repo)
    stock = use_case.create_stock("AAPL", "Apple Inc.", "Technology", "Consumer Electronics", 150.0, "2023-09-01")

    assert stock.ticker == "AAPL"
    assert stock.name == "Apple Inc."
    mock_stock_repo.create_stock.assert_called_once()

def test_update_stock(mock_stock_repo):
    # Mock the return value of get_stock_by_ticker
    mock_stock_repo.get_stock_by_ticker.return_value = Stock(
        "AAPL", "Apple Inc.", "Technology", "Consumer Electronics", 150.0, "2023-09-01"
    )

    # Create the use case instance
    use_case = ManageStockUseCase(stock_repository=mock_stock_repo)

    # Perform the update operation
    updated_stock = use_case.update_stock("AAPL", close_price=160.0)

    # Use pytest.approx for floating point comparison
    assert updated_stock.close_price == pytest.approx(160.0)
    
def test_delete_stock(mock_stock_repo):
    mock_stock_repo.get_stock_by_ticker.return_value = Stock("AAPL", "Apple Inc.", "Technology", "Consumer Electronics", 150.0, "2023-09-01")

    use_case = ManageStockUseCase(stock_repository=mock_stock_repo)
    result = use_case.delete_stock("AAPL")

    assert result is True
    mock_stock_repo.delete_stock.assert_called_once_with("AAPL")
    
    
def test_update_stock_not_found(mock_stock_repo):
    mock_stock_repo.get_stock_by_ticker.return_value = None  # Simulate stock not found

    stock_use_case = ManageStockUseCase(stock_repository=mock_stock_repo)
    
    with pytest.raises(ValueError, match="Stock with ticker AAPL not found"):
        stock_use_case.update_stock(ticker="AAPL", close_price=160.0)

def test_delete_stock_not_found(mock_stock_repo):
    mock_stock_repo.get_stock_by_ticker.return_value = None  # Simulate stock not found

    stock_use_case = ManageStockUseCase(stock_repository=mock_stock_repo)
    
    result = stock_use_case.delete_stock(ticker="AAPL")
    
    assert result is False
    mock_stock_repo.delete_stock.assert_not_called()
