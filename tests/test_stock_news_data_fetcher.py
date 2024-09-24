# test_stock_news_data_fetcher.py

import os
import pytest
import sqlite3
import tempfile
import shutil
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import logging
# Import the classes and main function from your script
from stock_news_data_fetcher import (
    FinnhubNewsFetcher,
    NewsDatabaseManager,
    main
)

# ============================
# Fixtures for Testing
# ============================

@pytest.fixture
def temp_db():
    """
    Creates a temporary database file for testing.
    """
    temp_dir = tempfile.mkdtemp()
    db_path = os.path.join(temp_dir, 'test_stock_news.db')

    # Return the path to the temporary database
    yield db_path

    # Explicitly close the connection to the database
    try:
        conn = sqlite3.connect(db_path)
        conn.close()
    except sqlite3.Error as e:
        logging.error(f"Error closing database connection: {e}")

    # Make sure the connection is closed and the directory is deleted
    try:
        shutil.rmtree(temp_dir)
    except PermissionError as e:
        logging.error(f"PermissionError while trying to remove directory: {e}")


@pytest.fixture
def news_fetcher():
    """
    Provides a FinnhubNewsFetcher instance with a mock API key.
    """
    return FinnhubNewsFetcher(api_key='test_api_key')

@pytest.fixture
def db_manager(temp_db):
    """
    Provides a NewsDatabaseManager instance connected to the temporary database.
    """
    return NewsDatabaseManager(db_name=temp_db)

@pytest.fixture
def sample_news_data():
    """
    Provides sample news data for testing.
    """
    return [
        {
            'headline': 'Test Headline 1',
            'source': 'Test Source',
            'datetime': int((datetime.now() - timedelta(days=1)).timestamp()),
            'summary': 'Test Summary 1',
            'url': 'http://example.com/1'
        },
        {
            'headline': 'Test Headline 2',
            'source': 'Test Source',
            'datetime': int((datetime.now() - timedelta(days=2)).timestamp()),
            'summary': 'Test Summary 2',
            'url': 'http://example.com/2'
        }
    ]

# ============================
# Tests
# ============================

def test_fetch_news(news_fetcher, sample_news_data):
    """
    Tests that fetch_news returns the expected data.
    """
    with patch.object(news_fetcher.client, 'company_news', return_value=sample_news_data) as mock_method:
        result = news_fetcher.fetch_news(symbol='AAPL', from_date='2022-01-01', to_date='2022-01-31')
        assert result == sample_news_data
        mock_method.assert_called_once_with('AAPL', _from='2022-01-01', to='2022-01-31')

def test_insert_news(db_manager, sample_news_data):
    """
    Tests that insert_news correctly inserts data into the database.
    """
    symbol = 'AAPL'
    inserted = db_manager.insert_news(symbol, sample_news_data)
    assert inserted == len(sample_news_data)
    
    # Verify data in database
    db_manager.cursor.execute("SELECT * FROM stock_news")
    rows = db_manager.cursor.fetchall()
    assert len(rows) == len(sample_news_data)
    db_manager.close()

def test_get_latest_datetime(db_manager, sample_news_data):
    """
    Tests that get_latest_datetime returns the correct latest datetime.
    """
    symbol = 'AAPL'
    db_manager.insert_news(symbol, sample_news_data)
    latest_datetime = db_manager.get_latest_datetime(symbol)
    expected_datetime = max(article['datetime'] for article in sample_news_data)
    assert latest_datetime == expected_datetime

def test_main_function_no_new_data(monkeypatch, temp_db):
    """
    Tests the main function when no new data is available.
    """
    # Mock FinnhubNewsFetcher to return empty list
    def mock_fetch_news(*args, **kwargs):
        return []

    # Mock NewsDatabaseManager to use temp_db
    def mock_db_manager(*args, **kwargs):
        return NewsDatabaseManager(db_name=temp_db)

    monkeypatch.setattr('stock_news_data_fetcher.FinnhubNewsFetcher.fetch_news', mock_fetch_news)
    monkeypatch.setattr('stock_news_data_fetcher.NewsDatabaseManager', mock_db_manager)
    monkeypatch.setattr('sys.argv', ['stock_news_data_fetcher.py'])

    # Run main function
    main()

    # Check that no new data was inserted
    db_manager = NewsDatabaseManager(db_name=temp_db)
    total_articles = db_manager.get_total_articles()
    assert total_articles == 0

def test_main_function_with_new_data(monkeypatch, temp_db, sample_news_data):
    """
    Tests the main function when new data is available.
    """
    # Mock FinnhubNewsFetcher to return sample_news_data
    def mock_fetch_news(*args, **kwargs):
        return sample_news_data

    # Mock NewsDatabaseManager to use temp_db
    def mock_db_manager(*args, **kwargs):
        return NewsDatabaseManager(db_name=temp_db)

    monkeypatch.setattr('stock_news_data_fetcher.FinnhubNewsFetcher.fetch_news', mock_fetch_news)
    monkeypatch.setattr('stock_news_data_fetcher.NewsDatabaseManager', mock_db_manager)
    monkeypatch.setattr('sys.argv', ['stock_news_data_fetcher.py'])

    # Run main function
    main()

    # Check that new data was inserted
    db_manager = NewsDatabaseManager(db_name=temp_db)
    total_articles = db_manager.get_total_articles()
    assert total_articles == len(sample_news_data)

def test_command_line_arguments(monkeypatch, temp_db, sample_news_data):
    """
    Tests that command-line arguments are parsed and used correctly.
    """
    # Mock FinnhubNewsFetcher to return sample_news_data
    def mock_fetch_news(*args, **kwargs):
        return sample_news_data

    # Mock NewsDatabaseManager to use temp_db
    def mock_db_manager(*args, **kwargs):
        return NewsDatabaseManager(db_name=temp_db)

    # Mock sys.argv to include command-line arguments
    monkeypatch.setattr('sys.argv', [
        'stock_news_data_fetcher.py',
        '--start-date', '2020-01-01',
        '--print-db'
    ])

    monkeypatch.setattr('stock_news_data_fetcher.FinnhubNewsFetcher.fetch_news', mock_fetch_news)
    monkeypatch.setattr('stock_news_data_fetcher.NewsDatabaseManager', mock_db_manager)

    # Mock print function to capture output
    with patch('builtins.print') as mock_print:
        main()

    # Check that data was inserted
    db_manager = NewsDatabaseManager(db_name=temp_db)
    total_articles = db_manager.get_total_articles()
    assert total_articles == len(sample_news_data)

    # Verify that print was called (since --print-db was specified)
    assert mock_print.called

def test_fetch_news_error_handling(news_fetcher):
    """
    Tests that fetch_news handles API exceptions gracefully.
    """
    with patch.object(news_fetcher.client, 'company_news', side_effect=Exception('API Error')):
        result = news_fetcher.fetch_news(symbol='AAPL', from_date='2022-01-01', to_date='2022-01-31')
        assert result == []

def test_insert_news_no_data(db_manager):
    """
    Tests that insert_news handles empty news list correctly.
    """
    symbol = 'AAPL'
    inserted = db_manager.insert_news(symbol, [])
    assert inserted == 0

def test_print_news_data(db_manager, sample_news_data):
    """
    Tests that print_news_data outputs the correct information.
    """
    db_manager.insert_news('AAPL', sample_news_data)
    
    # Mock print function to capture output
    with patch('builtins.print') as mock_print:
        db_manager.print_news_data()
        assert mock_print.call_count == len(sample_news_data)

def test_get_total_articles(db_manager, sample_news_data):
    """
    Tests that get_total_articles returns the correct count.
    """
    assert db_manager.get_total_articles() == 0
    db_manager.insert_news('AAPL', sample_news_data)
    assert db_manager.get_total_articles() == len(sample_news_data)
