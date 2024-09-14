# tests/test_database_manager.py

import pytest
import sqlite3
import os
from datetime import datetime
from stock_data_fetcher import DatabaseManager  # Adjust import as per your script
import logging  # Add this import


@pytest.fixture
def temp_db():
    """
    Creates a temporary database file for testing.
    """
    temp_dir = tempfile.mkdtemp()
    db_path = os.path.join(temp_dir, 'test_stock_news.db')

    # Yield the path to be used in the test
    yield db_path

    # Close the connection explicitly before removing the directory
    try:
        if os.path.exists(db_path):
            conn = sqlite3.connect(db_path)
            conn.close()
    except Exception as e:
        logging.error(f"Error closing the database connection: {e}")
    
    shutil.rmtree(temp_dir)

# Fixture for setting up and tearing down the database
@pytest.fixture
def db_manager():
    # Use an in-memory SQLite database for testing
    manager = DatabaseManager(db_name=':memory:')
    yield manager
    manager.close()

def test_create_table(db_manager):
    # Check if the table exists
    db_manager.cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='table' AND name='stock_prices';
    """)
    table_exists = db_manager.cursor.fetchone()
    assert table_exists is not None, "Table 'stock_prices' should exist."

def test_insert_data(db_manager):
    # Sample data
    symbol = 'TEST'
    timestamp = datetime.now().replace(microsecond=0)
    data = {
        'Datetime': [timestamp],
        'Open': [100.0],
        'High': [110.0],
        'Low': [90.0],
        'Close': [105.0],
        'Volume': [1000]
    }
    import pandas as pd
    df = pd.DataFrame(data)

    # Insert the data
    db_manager.insert_bulk_data(symbol, df, 'YahooFinance')

    # Fetch the inserted data to verify
    db_manager.cursor.execute("SELECT * FROM stock_prices WHERE symbol = ?", (symbol,))
    rows = db_manager.cursor.fetchall()

    # Log the rows for debugging
    logging.info(f"Fetched rows: {rows}")

    # Verify that one record was inserted
    assert len(rows) == 1, "One record should be inserted."

    # Close the connection
    db_manager.close()


def test_duplicate_handling(db_manager):
    # Initial data
    symbol = 'TEST'
    timestamp = datetime.now().replace(microsecond=0)
    data = {
        'Datetime': [timestamp],
        'Open': [100.0],
        'High': [110.0],
        'Low': [90.0],
        'Close': [105.0],
        'Volume': [1000]
    }
    import pandas as pd
    df = pd.DataFrame(data)

    # Use insert_bulk_data instead of insert_data
    db_manager.insert_bulk_data(symbol, df, 'YahooFinance')

    # Add assertions here to verify that the data was inserted correctly
    rows = db_manager.cursor.execute("SELECT * FROM stock_prices").fetchall()
    assert len(rows) == 1, "One record should be inserted."


def test_close(db_manager):
    db_manager.close()
    with pytest.raises(sqlite3.ProgrammingError):
        db_manager.cursor.execute("SELECT 1;")
