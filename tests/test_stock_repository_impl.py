import pytest
from unittest.mock import MagicMock
from src.infrastructure.db.stock_repository_impl import StockRepositoryImpl
from src.domain.models.stock import Stock
from datetime import datetime

@pytest.fixture
def db_session():
    # Mock the database session
    return MagicMock()

@pytest.fixture
def stock_repo(db_session):
    # Create an instance of StockRepositoryImpl with the mocked session
    return StockRepositoryImpl(db_session)

def test_create_stock(stock_repo, db_session):
    stock = Stock(ticker="AAPL", name="Apple", industry="Technology", sector="Consumer Electronics", close=150.0, date="2023-01-01")
    stock_repo.create_stock(stock)
    db_session.add.assert_called_once_with(stock)
    db_session.commit.assert_called_once()

def test_get_stock(stock_repo, db_session):
    mock_stock = Stock(ticker="AAPL", name="Apple", industry="Technology", sector="Consumer Electronics", close=145.0, date="2023-01-01")
    db_session.query().filter_by().first.return_value = mock_stock
    stock = stock_repo.get("AAPL")
    assert stock == mock_stock

def test_get_non_existent_stock(stock_repo, db_session):
    db_session.query().filter_by().first.return_value = None
    stock = stock_repo.get("NON_EXISTENT")
    assert stock is None

def test_update_stock(stock_repo, db_session):
    stock = Stock(ticker="AAPL", name="Apple", industry="Technology", sector="Consumer Electronics", close=150.0, date="2023-01-01")
    db_session.query().filter_by().first.return_value = stock
    stock_repo.update(stock)
    db_session.merge.assert_called_once_with(stock)
    db_session.commit.assert_called_once()

def test_delete_stock(stock_repo, db_session):
    mock_stock = Stock(ticker="AAPL", name="Apple", industry="Technology", sector="Consumer Electronics", close=145.0, date="2023-01-01")
    db_session.query().filter_by.return_value.first.return_value = mock_stock
    result = stock_repo.delete_stock("AAPL")
    assert result is True
    db_session.delete.assert_called_once_with(mock_stock)
    db_session.commit.assert_called_once()

def test_delete_non_existent_stock(stock_repo, db_session):
    db_session.query().filter_by.return_value.first.return_value = None
    result = stock_repo.delete_stock("NON_EXISTENT")
    assert result is False
    db_session.delete.assert_not_called()
    db_session.commit.assert_not_called()

def test_get_stock_data(stock_repo, db_session):
    mock_stock = Stock(ticker="AAPL", name="Apple", industry="Technology", sector="Consumer Electronics", close=150.0, date="2023-01-01")
    db_session.query.return_value.filter.return_value.all.return_value = [mock_stock]
    result = stock_repo.get_stock_data("AAPL", datetime(2022, 1, 1), datetime(2023, 1, 1), "daily")
    assert result == [mock_stock]

def test_stock_exists(stock_repo, db_session):
    # Properly mock scalar() to return True
    db_session.query.return_value.filter.return_value.exists.return_value = True
    db_session.query.return_value.scalar.return_value = True
    
    result = stock_repo.stock_exists("AAPL", "1y")
    assert result is True
    
def test_stock_does_not_exist(stock_repo, db_session):
    # Properly mock scalar() to return False
    db_session.query.return_value.filter.return_value.exists.return_value = False
    db_session.query.return_value.scalar.return_value = False
    
    result = stock_repo.stock_exists("AAPL", "1y")
    assert result is False

def test_get_sample_stock_data(stock_repo, db_session):
    mock_stock = Stock(ticker="AAPL", name="Apple", industry="Technology", sector="Consumer Electronics", close=150.0, date="2023-01-01")
    db_session.query().filter_by().limit().all.return_value = [mock_stock]
    result = stock_repo.get_sample_stock_data("AAPL")
    assert result == [mock_stock]

def test_add_stock(stock_repo, db_session):
    mock_stock = Stock(ticker="AAPL", name="Apple", industry="Technology", sector="Consumer Electronics", close=150.0, date="2023-01-01")
    stock_repo.add_stock(mock_stock)
    db_session.add.assert_called_once_with(mock_stock)

def test_commit(stock_repo, db_session):
    stock_repo.commit()
    db_session.commit.assert_called_once()

def test_get_date_range_for_period(stock_repo):
    start_date, end_date = stock_repo.get_date_range_for_period("1y")
    assert start_date < end_date

    with pytest.raises(ValueError):
        stock_repo.get_date_range_for_period("invalid_period")
