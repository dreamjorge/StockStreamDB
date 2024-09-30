from math import isclose
import pytest
from unittest.mock import MagicMock
from src.application.use_cases.manage_stock import ManageStockUseCase
from src.domain.models.stock import Stock


@pytest.fixture
def manage_stock_use_case(stock_repo):
    return ManageStockUseCase(stock_repository=stock_repo)


def test_create_stock(manage_stock_use_case, stock_repo):
    # Mock the repository method create_stock
    stock_repo.create_stock = MagicMock()

    # Create a new stock
    stock = manage_stock_use_case.create_stock(
        ticker="AAPL",
        name="Apple Inc.",
        industry="Technology",
        sector="Consumer Electronics",
        close_price=150.0,
        date="2023-09-01"
    )

    # Assert the stock was created with correct attributes
    assert stock.ticker == "AAPL"
    assert stock.name == "Apple Inc."
    assert stock.industry == "Technology"
    assert stock.sector == "Consumer Electronics"
    assert isclose(stock.close_price, 150.0, rel_tol=1e-9)
    assert stock.date == "2023-09-01"

    # Ensure repository's create_stock method was called with the correct stock object
    stock_repo.create_stock.assert_called_once_with(stock)


def test_delete_stock_not_found(manage_stock_use_case, stock_repo):
    # Mock the return value of get_by_ticker to simulate stock not found
    stock_repo.get_by_ticker = MagicMock(return_value=None)
    
    # Mock the delete_stock function to ensure it can be asserted
    stock_repo.delete_stock = MagicMock()

    # Call the delete method
    result = manage_stock_use_case.delete_stock("NON_EXISTENT")

    # Ensure that the method returns False when the stock is not found
    assert result is False

    # Ensure delete_stock was not called
    stock_repo.delete_stock.assert_not_called()


def test_delete_stock_success(manage_stock_use_case, stock_repo, mock_stock):
    # Mock the return value of get_by_ticker to simulate stock found
    stock_repo.get_by_ticker = MagicMock(return_value=Stock(**mock_stock))
    stock_repo.delete_stock = MagicMock(return_value=True)  # Ensure delete_stock call succeeds

    # Call the delete method and assert success
    result = manage_stock_use_case.delete_stock("AAPL")
    assert result is True  # The stock should be deleted
    stock_repo.delete_stock.assert_called_once_with("AAPL")


def test_update_stock_fields(manage_stock_use_case, stock_repo, mock_stock):
    # Simulate an existing stock found in the repository
    stock_repo.get_by_ticker = MagicMock(return_value=Stock(**mock_stock))
    
    # Mock the update method
    stock_repo.update = MagicMock()

    # Call update_stock method to update multiple fields
    updated_stock = manage_stock_use_case.update_stock(
        ticker="AAPL", close_price=160.0, name="New Name", industry="New Industry", sector="New Sector"
    )

    # Ensure the fields were updated correctly
    assert updated_stock.close_price == 160.0
    assert updated_stock.name == "New Name"
    assert updated_stock.industry == "New Industry"
    assert updated_stock.sector == "New Sector"

    # Ensure the stock repository update method was called
    stock_repo.update.assert_called_once_with(updated_stock)


def test_fetch_stock_data(manage_stock_use_case, stock_fetcher):
    # Mock the stock fetcher to return dummy data
    stock_fetcher.fetch = MagicMock(return_value={'ticker': 'AAPL', 'close_price': 150.0})
    manage_stock_use_case.stock_fetcher = stock_fetcher

    # Call the fetch_stock_data method
    result = manage_stock_use_case.fetch_stock_data(ticker="AAPL", period="1mo")

    # Assert that the fetcher returned data
    assert result == {'ticker': 'AAPL', 'close_price': 150.0}
    stock_fetcher.fetch.assert_called_once_with("AAPL", "1mo")


def test_fetch_stock_data_no_data(manage_stock_use_case, stock_fetcher):
    # Mock the stock fetcher to return None (to simulate no data being fetched)
    stock_fetcher.fetch = MagicMock(return_value=None)
    manage_stock_use_case.stock_fetcher = stock_fetcher

    # Call the fetch_stock_data method
    result = manage_stock_use_case.fetch_stock_data(ticker="AAPL", period="1mo")

    # Assert that the fetch_stock_data method returns None when no data is fetched
    assert result is None, "The fetch_stock_data method should return None when no data is available."
    stock_fetcher.fetch.assert_called_once_with("AAPL", "1mo")


def test_update_stock_repository_called(manage_stock_use_case, stock_repo, mock_stock):
    # Mock an existing stock
    stock_repo.get_by_ticker = MagicMock(return_value=Stock(**mock_stock))

    # Mock the update method
    stock_repo.update = MagicMock()

    # Call update_stock method
    updated_stock = manage_stock_use_case.update_stock(ticker="AAPL", close_price=160.0)

    # Ensure that the stock repository update method was called
    stock_repo.update.assert_called_once_with(updated_stock)


def test_update_stock_no_updates(manage_stock_use_case, stock_repo, mock_stock):
    # Simulate an existing stock found in the repository by mocking get_by_ticker
    stock_repo.get_by_ticker = MagicMock(return_value=Stock(**mock_stock))
    
    # Mock the update method to ensure it's callable
    stock_repo.update = MagicMock()

    # Call update_stock without any fields to update
    updated_stock = manage_stock_use_case.update_stock(ticker="AAPL")

    # Ensure the stock returned is the same without updates
    assert updated_stock.ticker == "AAPL"
    assert updated_stock.close_price == 150.0  # Ensure old value is unchanged
    assert updated_stock.name == "Apple"  # Ensure old value is unchanged

    # Ensure repository's update method was called
    stock_repo.update.assert_called_once_with(updated_stock)


def test_delete_stock_failure(manage_stock_use_case, stock_repo):
    # Mock the return value of get_by_ticker to simulate stock not found
    stock_repo.get_by_ticker = MagicMock(return_value=None)
    
    # Mock delete_stock to make it a MagicMock
    stock_repo.delete_stock = MagicMock()

    # Call the delete method and assert failure
    result = manage_stock_use_case.delete_stock("AAPL")
    assert result is False  # The stock should not be deleted
    
    # Ensure delete_stock was not called
    stock_repo.delete_stock.assert_not_called()
