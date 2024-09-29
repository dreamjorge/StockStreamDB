import pytest
from unittest.mock import MagicMock
from src.infrastructure.db.stock_repository_impl import StockRepositoryImpl
from src.domain.models.stock import Stock

@pytest.fixture
def db_session():
    # Mock the database session
    return MagicMock()

@pytest.fixture
def stock_repo(db_session):
    # Create an instance of StockRepositoryImpl with the mocked session
    return StockRepositoryImpl(db_session)

def test_create_stock(stock_repo, db_session):
    # Mock stock object
    stock = Stock(ticker="AAPL", name="Apple", industry="Technology", sector="Consumer Electronics", close_price=150.0, date="2023-01-01")
    
    # Call create_stock
    stock_repo.create_stock(stock)
    
    # Verify that the session's add and commit methods were called
    db_session.add.assert_called_once_with(stock)
    db_session.commit.assert_called_once()

def test_get_stock(stock_repo, db_session):
    # Mock stock object
    mock_stock = Stock(ticker="AAPL", name="Apple", industry="Technology", sector="Consumer Electronics", close_price=145.0, date="2023-01-01")
    
    # Configure the session query to return the mock stock
    db_session.query().filter().first.return_value = mock_stock
    
    # Call get and verify result
    stock = stock_repo.get("AAPL")
    assert stock == mock_stock
    db_session.query().filter().first.assert_called_once()

def test_update_stock(stock_repo, db_session):
    # Mock stock object
    stock = Stock(ticker="AAPL", name="Apple", industry="Technology", sector="Consumer Electronics", close_price=150.0, date="2023-01-01")
    
    # Call update
    stock_repo.update(stock)
    
    # Verify session's merge and commit methods were called
    db_session.merge.assert_called_once_with(stock)
    db_session.commit.assert_called_once()

def test_delete_stock(stock_repo, db_session):
    # Mock stock object
    mock_stock = Stock(ticker="AAPL", name="Apple", industry="Technology", sector="Consumer Electronics", close_price=145.0, date="2023-01-01")

    # Ensure the query chain returns the correct mock_stock object
    mock_query = db_session.query.return_value
    mock_query.filter_by.return_value.first.return_value = mock_stock  # Correctly mock filter_by().first()

    # Call delete_stock
    result = stock_repo.delete_stock("AAPL")

    # Verify that delete was called with the correct stock object
    assert result is True
    db_session.delete.assert_called_once_with(mock_stock)
    db_session.commit.assert_called_once()






