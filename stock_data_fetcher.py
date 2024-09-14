import os
import time
import sqlite3
import requests
import yfinance as yf
import logging
from datetime import datetime, timedelta
from abc import ABC, abstractmethod

# Setup logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ==============================
# Abstract Base Class for Fetcher
# ==============================

class StockDataFetcher(ABC):
    @abstractmethod
    def fetch_intraday_data(self, symbol):
        """
        Fetch intraday stock data for a given symbol.
        Returns:
            DataFrame or dict: Intraday stock data.
        """
        pass

# ============================
# Yahoo Finance Fetcher
# ============================

class YFPricesMissingError(Exception):
    """Custom exception for missing prices in Yahoo Finance."""
    pass

class YahooFinanceFetcher:
    """
    Fetches intraday stock data using the Yahoo Finance API.
    """
    def fetch_intraday_data(self, symbol, interval='1m', last_timestamp=None):
        """
        Fetches intraday stock data from Yahoo Finance.
        
        Args:
            symbol (str): The stock symbol to fetch data for.
            interval (str): Time interval between data points (default: '1m').
            last_timestamp (str): Optional. Fetch data after this timestamp.

        Returns:
            DataFrame: Intraday stock data.
        """
        # Always use '1d' period for fetching intraday data
        period = '1d'

        try:
            # Fetch data using yfinance
            data = yf.download(tickers=symbol, period=period, interval=interval)
            data.index.name = 'Datetime'
            data.reset_index(inplace=True)

            # If no data is returned, raise a custom exception
            if data.empty:
                raise YFPricesMissingError(f"No prices found for {symbol} in the requested period.")
            
            # If last_timestamp is provided, filter out older data
            if last_timestamp is not None:
                data = data[data['Datetime'] > last_timestamp]

            return data

        except Exception as e:
            logging.error(f"An error occurred while fetching data for {symbol}: {e}")
            return None

# ============================
# Database Manager Class
# ============================

class DatabaseManager:
    """
    Manages the SQLite database for storing stock price data.
    """
    def __init__(self, db_name='stock_data.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS stock_prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                timestamp DATETIME NOT NULL,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume INTEGER,
                UNIQUE(symbol, timestamp)
            )
        """)
        self.conn.commit()

    def insert_bulk_data(self, symbol, data, source):
        """
        Inserts stock data in bulk into the database.
        """
        if source == 'YahooFinance' and not data.empty:
            rows = [
                (
                    symbol,
                    row['Datetime'].strftime('%Y-%m-%d %H:%M:%S'),
                    row['Open'],
                    row['High'],
                    row['Low'],
                    row['Close'],
                    row['Volume']
                ) for index, row in data.iterrows()
            ]
            self.cursor.executemany("""
                INSERT INTO stock_prices (symbol, timestamp, open, high, low, close, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(symbol, timestamp) DO UPDATE SET
                    open=excluded.open,
                    high=excluded.high,
                    low=excluded.low,
                    close=excluded.close,
                    volume=excluded.volume
            """, rows)
            # Add this commit call to ensure the data is written to the database
            self.conn.commit()


    def get_last_timestamp(self, symbol):
        """
        Fetches the last recorded timestamp for a given stock symbol.
        
        Args:
            symbol (str): The stock symbol.

        Returns:
            str or None: The last timestamp or None if no data exists.
        """
        self.cursor.execute("""
            SELECT MAX(timestamp) FROM stock_prices WHERE symbol = ?
        """, (symbol,))
        result = self.cursor.fetchone()
        return result[0] if result and result[0] else None

    def close(self):
        self.conn.close()

# ============================
# Main Function
# ============================

def main():
    """
    Main function to fetch and store stock data from various sources.
    """
    fetcher_type = 'YahooFinance'
    symbol = 'AAPL'
    
    # Initialize the fetcher and database manager
    fetcher = YahooFinanceFetcher()
    db_manager = DatabaseManager()

    try:
        while True:
            logging.info(f"Fetching data for {symbol} using {fetcher_type}")

            # Get the last timestamp to only fetch new data
            last_timestamp = db_manager.get_last_timestamp(symbol)

            # Fetch new data after the last timestamp
            data = fetcher.fetch_intraday_data(symbol, last_timestamp=last_timestamp)
            if data is not None and not data.empty:
                db_manager.insert_bulk_data(symbol, data, fetcher_type)
                logging.info(f"Inserted {len(data)} records for {symbol} using {fetcher_type}")
            else:
                logging.info("No new data fetched.")
            time.sleep(60)  # Wait for 1 minute before fetching again
    except KeyboardInterrupt:
        logging.info("Stopping data fetch...")
    finally:
        db_manager.close()

if __name__ == '__main__':
    main()
