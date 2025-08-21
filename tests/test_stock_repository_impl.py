import pytest
from unittest.mock import MagicMock
from src.infrastructure.db.stock_repository_impl import (
    StockRepositoryImpl,
    to_domain,
    to_persistence,
)
from src.domain.models.stock import Stock
from src.infrastructure.db.models import StockDB
from datetime import datetime


@pytest.fixture
def db_session():
    # Mock the database session
    return MagicMock()


@pytest.fixture
def stock_repo(db_session):
    # Create an instance of StockRepositoryImpl with the mocked session
    return StockRepositoryImpl(db_session)


@pytest.fixture
def mock_stock():
    return Stock(
        id=1,
        ticker="AAPL",
        name="Apple Inc.",
        industry="Technology",
        sector="Consumer Electronics",
        date=datetime(2024, 1, 1),
        close=150.0,
    )


@pytest.fixture
def mock_stock_db():
    return StockDB(
        id=1,
        ticker="AAPL",
        name="Apple Inc.",
        industry="Technology",
        sector="Consumer Electronics",
        date=datetime(2024, 1, 1),
        close=150.0,
    )


def test_add_stock(stock_repo, db_session, mock_stock, mock_stock_db):
    stock_repo.add(mock_stock)
    db_session.add.assert_called_once()
    db_session.commit.assert_called_once()


def test_get_by_ticker(stock_repo, db_session, mock_stock, mock_stock_db):
    db_session.query().filter_by().first.return_value = mock_stock_db
    stock = stock_repo.get_by_ticker("AAPL")
    assert stock == mock_stock


def test_get_non_existent_stock(stock_repo, db_session):
    db_session.query().filter_by().first.return_value = None
    stock = stock_repo.get_by_ticker("NON_EXISTENT")
    assert stock is None


def test_update_stock(stock_repo, db_session, mock_stock, mock_stock_db):
    db_session.query().filter_by().first.return_value = mock_stock_db
    stock_repo.update(mock_stock)
    db_session.commit.assert_called_once()


def test_delete_stock(stock_repo, db_session, mock_stock_db):
    db_session.query().filter_by().first.return_value = mock_stock_db
    stock_repo.delete("AAPL")
    db_session.delete.assert_called_once_with(mock_stock_db)
    db_session.commit.assert_called_once()
