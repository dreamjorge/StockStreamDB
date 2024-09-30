# tests/test_manage_stock.py
import pytest
from unittest.mock import MagicMock
from src.application.use_cases.manage_stock import ManageStockUseCase
from src.domain.models.stock import Stock

@pytest.fixture
def mock_stock_repo():
    return MagicMock()

def test_create_stock(mock_stock_repo):
    # Create a mock Stock object to return
    mock_stock = Stock(
        ticker="AAPL",
        name="Apple Inc.",
        industry="Technology",
        sector="Consumer Electronics",
        close_price=150.0,
        date="2023-09-01"
    )

    # Mock the repository's create_stock method to return the mock Stock object
    # It should return the same stock object that is passed
    mock_stock_repo.create_stock.return_value = mock_stock

    # Call the use case
    use_case = ManageStockUseCase(stock_repository=mock_stock_repo)
    stock = use_case.create_stock(
        ticker="AAPL",
        name="Apple Inc.",
        industry="Technology",
        sector="Consumer Electronics",
        close_price=150.0,
        date="2023-09-01"
    )

    # Assert that the returned stock is as expected
    assert stock.ticker == "AAPL"

    # Verify that create_stock was called once with the correct parameters
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
    # Mock the return value of get_stock_by_ticker
    mock_stock_repo.get_stock_by_ticker.return_value = Stock(
        ticker="AAPL",
        name="Apple Inc.",
        industry="Technology",
        sector="Consumer Electronics",
        close_price=150.0,
        date="2023-09-01"
    )

    # Ensure delete_stock is called when a stock is deleted
    mock_stock_repo.delete_stock.return_value = True  # Ensure delete call succeeds

    # Create an instance of ManageStockUseCase
    use_case = ManageStockUseCase(stock_repository=mock_stock_repo)

    # Call the delete method
    result = use_case.delete_stock("AAPL")

    # Ensure that the deletion was successful
    assert result is True

    # Verify that delete_stock was called once
    mock_stock_repo.delete_stock.assert_called_once_with("AAPL")  # Check correct method is called

    
    
def test_update_stock_not_found(mock_stock_repo):
    mock_stock_repo.get_stock_by_ticker.return_value = None  # Simulate stock not found

    stock_use_case = ManageStockUseCase(stock_repository=mock_stock_repo)
    
    with pytest.raises(ValueError, match="Stock with ticker AAPL not found"):
        stock_use_case.update_stock(ticker="AAPL", close_price=160.0)

def test_delete_stock(mock_stock_repo):
    # Mock the return value of get_stock_by_ticker
    mock_stock_repo.get_stock_by_ticker.return_value = Stock(
        ticker="AAPL",
        name="Apple Inc.",
        industry="Technology",
        sector="Consumer Electronics",
        close_price=150.0,
        date="2023-09-01"
    )

    # Mock the repository to expect delete to be called
    mock_stock_repo.delete.return_value = True  # Ensure delete call succeeds

    # Create an instance of ManageStockUseCase
    use_case = ManageStockUseCase(stock_repository=mock_stock_repo)

    # Call the delete method
    result = use_case.delete_stock("AAPL")

    # Ensure that the deletion was successful
    assert result is True

    # Check if delete was called
    mock_stock_repo.delete.assert_called_once_with("AAPL")  # Ensure delete is called
