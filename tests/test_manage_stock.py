from math import isclose
import pytest
from unittest.mock import MagicMock
from src.application.use_cases.manage_stock import ManageStockUseCase
from src.domain.models.stock import Stock
from datetime import date  # Add this import


@pytest.fixture
def stock_repo():
    # Mock the StockRepository
    return MagicMock()


@pytest.fixture
def stock_fetcher():
    # Mock the StockFetcher
    return MagicMock()


@pytest.fixture
def mock_stock():
    # Provide a mock stock object
    return {
        "ticker": "AAPL",
        "name": "Apple",
        "industry": "Technology",
        "sector": "Consumer Electronics",
        "close": 150.0,
        "date": "2023-09-01",
    }


@pytest.fixture
def manage_stock_use_case(stock_repo, stock_fetcher):
    # Inject the stock_repo and stock_fetcher into the use case
    return ManageStockUseCase(stock_repo=stock_repo, stock_fetcher=stock_fetcher)


def test_create_stock(manage_stock_use_case, stock_repo):
    # Mock the repository method create_stock
    stock_repo.create_stock = MagicMock()

    # Create a new stock using positional arguments
    stock = manage_stock_use_case.create_stock(
        "AAPL",  # ticker
        "Apple Inc.",  # name
        "Technology",  # industry
        "Consumer Electronics",  # sector
        150.0,  # close
        "2023-09-01",  # date
    )

    # Assert the stock was created with correct attributes
    assert stock.ticker == "AAPL"
    assert stock.name == "Apple Inc."
    assert stock.industry == "Technology"
    assert stock.sector == "Consumer Electronics"
    assert isclose(stock.close, 150.0, rel_tol=1e-9)
    assert stock.date == "2023-09-01"

    # Assert that the save method was called correctly on the repository
    stock_repo.save.assert_called_once()

    # Assert that commit was called after saving
    stock_repo.commit.assert_called_once()


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
    stock = Stock(**mock_stock)
    stock_repo.get_by_ticker = MagicMock(return_value=stock)
    stock_repo.delete = MagicMock(
        return_value=True
    )  # Mock delete method instead of delete_stock

    # Call the delete method and assert success
    result = manage_stock_use_case.delete_stock("AAPL")
    assert result is True  # The stock should be deleted

    # Assert that delete was called with the correct stock (checking
    # attributes, not identity)
    stock_repo.delete.assert_called_once()
    args = stock_repo.delete.call_args[0]
    assert args[0].ticker == stock.ticker  # Compare attributes, not the object itself
    assert args[0].close == stock.close


def test_update_stock_fields(manage_stock_use_case, stock_repo, mock_stock):
    # Simulate an existing stock found in the repository
    stock_repo.get_by_ticker = MagicMock(return_value=Stock(**mock_stock))

    # Mock the update method
    stock_repo.update = MagicMock()

    # Call update_stock method to update multiple fields
    updated_stock = manage_stock_use_case.update_stock(
        ticker="AAPL",
        close=160.0,
        name="New Name",
        industry="New Industry",
        sector="New Sector",
    )

    # Ensure the fields were updated correctly
    assert isclose(updated_stock.close, 160.0, rel_tol=1e-9)
    assert updated_stock.name == "New Name"
    assert updated_stock.industry == "New Industry"
    assert updated_stock.sector == "New Sector"

    # Ensure the stock repository update method was called
    stock_repo.update.assert_called_once_with(updated_stock)


def test_fetch_stock_data(manage_stock_use_case, stock_fetcher):
    # Mock the stock fetcher to return a list of dictionaries with all required keys
    stock_fetcher.fetch = MagicMock(
        return_value=[
            {
                "ticker": "AAPL",
                "close": 150.0,
                "date": date(2023, 9, 1),  # Date as datetime.date object
                "open": 148.0,
                "high": 151.0,
                "low": 147.0,
                "volume": 1000000,
            }
        ]
    )
    manage_stock_use_case.stock_fetcher = stock_fetcher

    # Call the fetch_stock_data method
    result = manage_stock_use_case.fetch_stock_data(ticker="AAPL", period="1mo")

    # Assert that the fetcher returned data, compare with datetime.date
    assert result == [
        {
            "ticker": "AAPL",
            "close": 150.0,
            "date": date(2023, 9, 1),  # Compare against a datetime.date object
            "open": 148.0,
            "high": 151.0,
            "low": 147.0,
            "volume": 1000000,
        }
    ]
    stock_fetcher.fetch.assert_called_once_with("AAPL", "1mo")


def test_fetch_stock_data_no_data(manage_stock_use_case, stock_fetcher):
    # Mock the stock fetcher to return None (to simulate no data being fetched)
    stock_fetcher.fetch = MagicMock(return_value=None)
    manage_stock_use_case.stock_fetcher = stock_fetcher

    # Call the fetch_stock_data method
    result = manage_stock_use_case.fetch_stock_data(ticker="AAPL", period="1mo")

    # Assert that the fetch_stock_data method returns None when no data is fetched
    assert (
        result is None
    ), "The fetch_stock_data method should return None when no data is available."
    stock_fetcher.fetch.assert_called_once_with("AAPL", "1mo")


def test_update_stock_repository_called(manage_stock_use_case, stock_repo, mock_stock):
    # Mock an existing stock
    stock_repo.get_by_ticker = MagicMock(return_value=Stock(**mock_stock))

    # Mock the update method
    stock_repo.update = MagicMock()

    # Call update_stock method
    updated_stock = manage_stock_use_case.update_stock(ticker="AAPL", close=160.0)

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
    assert isclose(updated_stock.close, 150.0, rel_tol=1e-9)
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
