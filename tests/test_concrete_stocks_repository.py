import pytest
from unittest.mock import MagicMock
from datetime import datetime
from src.infrastructure.db.concrete_stocks_repository import ConcreteStocksRepository
from src.interfaces.common.enums import Granularity
import pandas as pd
from src.infrastructure.db.models import Stock  # Import the Stock model

# Fixtures for the mock session and repository


@pytest.fixture
def mock_session():
    return MagicMock()


@pytest.fixture
def stock_repository(mock_session):
    return ConcreteStocksRepository(session=mock_session)  # Pass mock session here


# Sample stock data
@pytest.fixture
def sample_stock():
    return Stock(
        ticker="AAPL",
        name="Apple Inc.",
        industry="Technology",
        sector="Consumer Electronics",
        date=datetime(2024, 9, 26),
        close=150.0,
    )


def test_get_stock_data(stock_repository, mock_session):
    # Prepare sample data
    sample_stock_data = [
        Stock(
            ticker="AAPL",
            name="Apple Inc.",
            industry="Technology",
            sector="Consumer Electronics",
            date=datetime(2024, 9, 26),
            close=150.0,
        ),
        Stock(
            ticker="AAPL",
            name="Apple Inc.",
            industry="Technology",
            sector="Consumer Electronics",
            date=datetime(2024, 9, 27),
            close=155.0,
        ),
        Stock(
            ticker="AAPL",
            name="Apple Inc.",
            industry="Technology",
            sector="Consumer Electronics",
            date=datetime(2024, 9, 28),
            close=160.0,
        ),
    ]

    # Mock the query result to return sample stock data
    mock_session.query().filter().all.return_value = sample_stock_data

    # Call the get_stock_data method
    start_date = datetime(2024, 9, 26)
    end_date = datetime(2024, 9, 28)
    df = stock_repository.get_stock_data(
        "AAPL", start_date, end_date, Granularity.DAILY
    )

    # Assert the DataFrame has the correct data
    expected_df = pd.DataFrame(
        {
            "date": pd.to_datetime(
                [datetime(2024, 9, 26), datetime(2024, 9, 27), datetime(2024, 9, 28)]
            ),
            "price": [150.0, 155.0, 160.0],
        }
    )

    pd.testing.assert_frame_equal(df.reset_index(drop=True), expected_df)


def test_get_stock_data_no_data(stock_repository, mock_session):
    # Mock the query result to return no data
    mock_session.query().filter().all.return_value = []

    # Call the get_stock_data method and expect a ValueError
    start_date = datetime(2024, 9, 26)
    end_date = datetime(2024, 9, 28)
    with pytest.raises(ValueError) as excinfo:
        stock_repository.get_stock_data("AAPL", start_date, end_date, Granularity.DAILY)
    assert "No data found for ticker AAPL" in str(excinfo.value)


def test_create_stock(stock_repository, mock_session, sample_stock):
    # Call the create_stock method
    stock_repository.create_stock(sample_stock)

    # Assert that session.add and session.commit were called
    mock_session.add.assert_called_once_with(sample_stock)
    mock_session.commit.assert_called_once()


def test_delete_stock_existing(stock_repository, mock_session, sample_stock):
    # Mock the query to return the actual sample stock
    mock_session.query().filter_by().first.return_value = sample_stock

    # Call the delete_stock method
    stock_repository.delete_stock("AAPL")

    # Assert that session.delete and session.commit were called with the correct stock
    mock_session.delete.assert_called_once_with(sample_stock)
    mock_session.commit.assert_called_once()


def test_delete_stock_non_existing(stock_repository, mock_session):
    # Mock the query to return None (no stock found)
    mock_session.query().filter_by().first.return_value = None

    # Call the delete_stock method
    stock_repository.delete_stock("AAPL")

    # Assert that session.delete was not called
    mock_session.delete.assert_not_called()
    mock_session.commit.assert_not_called()


def test_get_existing_stock(stock_repository, mock_session, sample_stock):
    # Mock the query to return the sample stock
    mock_session.query().filter_by().first.return_value = sample_stock

    # Call the get method
    result = stock_repository.get("AAPL")

    # Assert that the result is the sample stock
    assert result == sample_stock


def test_get_non_existing_stock(stock_repository, mock_session):
    # Mock the query to return None (no stock found)
    mock_session.query().filter_by().first.return_value = None

    # Call the get method
    result = stock_repository.get("AAPL")

    # Assert that the result is None
    assert result is None


def test_save_stock(stock_repository, mock_session, sample_stock):
    # Call the save method
    stock_repository.save(sample_stock)

    # Assert that session.add and session.commit were called
    mock_session.add.assert_called_once_with(sample_stock)
    mock_session.commit.assert_called_once()


def test_update_stock(stock_repository, mock_session, sample_stock):
    # Call the update method
    stock_repository.update(sample_stock)

    # Assert that session.merge and session.commit were called
    mock_session.merge.assert_called_once_with(sample_stock)
    mock_session.commit.assert_called_once()
