import os
import time
import sqlite3
import finnhub
import logging
import argparse
from datetime import datetime, timedelta

# Setup logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ============================
# Finnhub News Fetcher Class
# ============================

class FinnhubNewsFetcher:
    """
    Fetches financial news using the Finnhub API.
    """
    def __init__(self, api_key):
        self.client = finnhub.Client(api_key=api_key)

    def fetch_news(self, symbol=None, from_date=None, to_date=None):
        """
        Fetches news articles related to the stock market or a specific stock symbol.
        
        Args:
            symbol (str): The stock symbol to fetch news for (optional).
            from_date (str): Start date in 'YYYY-MM-DD' format.
            to_date (str): End date in 'YYYY-MM-DD' format.
        
        Returns:
            list: A list of news articles.
        """
        try:
            if symbol:
                logging.info(f"Fetching news for {symbol} from {from_date} to {to_date}")
                return self.client.company_news(symbol, _from=from_date, to=to_date)
            else:
                logging.info("Fetching general market news")
                return self.client.general_news('general')

        except Exception as e:
            logging.error(f"Error fetching news: {e}")
            return []

# ============================
# Database Manager Class
# ============================

class NewsDatabaseManager:
    """
    Manages the SQLite database for storing stock market news articles.
    """
    def __init__(self, db_name='stock_news.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def close(self):
        if self.conn:
            self.conn.close()

    def create_table(self):
        """
        Creates the news table if it doesn't exist.
        """
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS stock_news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT,
                headline TEXT,
                source TEXT,
                datetime INTEGER,
                summary TEXT,
                url TEXT,
                UNIQUE(symbol, headline, datetime)
            )
        """)
        self.conn.commit()

    def insert_news(self, symbol, news_list):
        """
        Inserts news articles into the database.
        
        Args:
            symbol (str): The stock symbol.
            news_list (list): List of news articles to insert.
        """
        total_inserted = 0
        if news_list:
            rows = [
                (
                    symbol,
                    article['headline'],
                    article['source'],
                    article['datetime'],  # Store as integer timestamp
                    article['summary'],
                    article['url']
                ) for article in news_list
            ]
            self.cursor.executemany("""
                INSERT OR IGNORE INTO stock_news (symbol, headline, source, datetime, summary, url)
                VALUES (?, ?, ?, ?, ?, ?)
            """, rows)
            self.conn.commit()
            total_inserted = self.cursor.rowcount
        return total_inserted

    def get_total_articles(self):
        """
        Returns the total number of articles in the database.
        """
        self.cursor.execute("SELECT COUNT(*) FROM stock_news")
        result = self.cursor.fetchone()
        return result[0] if result else 0

    def get_latest_datetime(self, symbol):
        """
        Gets the latest datetime of news for the given symbol.
        Returns None if no news for the symbol.
        """
        self.cursor.execute("""
            SELECT MAX(datetime) FROM stock_news WHERE symbol=?
        """, (symbol,))
        result = self.cursor.fetchone()
        if result and result[0]:
            latest_datetime = result[0]
            # Handle both INTEGER and TEXT datetime formats
            if isinstance(latest_datetime, int):
                return latest_datetime
            else:
                # Attempt to parse the datetime string
                try:
                    dt_obj = datetime.strptime(latest_datetime, '%Y-%m-%d %H:%M:%S')
                    return int(dt_obj.timestamp())
                except ValueError:
                    logging.error(f"Invalid datetime format in database: {latest_datetime}")
                    return None
        else:
            return None

    def print_news_data(self):
        """
        Retrieves and prints all news articles stored in the database.
        """
        try:
            self.cursor.execute("SELECT * FROM stock_news")
            rows = self.cursor.fetchall()

            if rows:
                logging.info(f"Total news articles: {len(rows)}")
                for row in rows:
                    date_str = datetime.fromtimestamp(row[4]).strftime('%Y-%m-%d %H:%M:%S')
                    print(f"ID: {row[0]}, Symbol: {row[1]}, Headline: {row[2]}, Source: {row[3]}, Date: {date_str}")
            else:
                logging.info("No news data found in the database.")

        except sqlite3.Error as e:
            logging.error(f"Error retrieving news data: {e}")

    def close(self):
        """
        Closes the database connection.
        """
        self.conn.close()

# ============================
# Main Function
# ============================

def main():
    """
    Main function to fetch and store stock market news.
    """
    parser = argparse.ArgumentParser(description='Fetch and store stock market news.')
    parser.add_argument('--start-date', type=str, default='2022-01-01', help='Start date in YYYY-MM-DD format')
    parser.add_argument('--print-db', action='store_true', help='Print the news data stored in the database')
    args = parser.parse_args()

    # Set up Finnhub API key and symbol
    api_key = os.getenv('FINNHUB_API_KEY', 'crib06hr01qqt33rgoh0crib06hr01qqt33rgohg')  # Replace with your actual API key
    symbol = os.getenv('STOCK_SYMBOL', 'AAPL')  # Default to Apple news, but can fetch for others

    if not api_key or api_key == 'your_actual_finnhub_api_key':
        logging.error("Finnhub API key is not set or invalid.")
        return

    # Initialize the fetcher and database manager
    news_fetcher = FinnhubNewsFetcher(api_key)
    db_manager = NewsDatabaseManager()

    start_date = args.start_date  # Use the start date from command-line argument

    try:
        # Get the latest datetime for the symbol
        latest_timestamp = db_manager.get_latest_datetime(symbol)
        if latest_timestamp:
            from_date = datetime.fromtimestamp(latest_timestamp)
            logging.info(f"Latest news datetime for {symbol} in database: {from_date}")
        else:
            from_date = datetime.strptime(start_date, '%Y-%m-%d')
            logging.info(f"No existing data for {symbol}. Starting from {start_date}")

        to_date = datetime.now()

        # Fetch data in batches
        current_date = from_date
        delta = timedelta(days=360)  # Adjust the delta as needed
        total_articles_added = 0

        while current_date < to_date:
            batch_from_date = current_date.strftime('%Y-%m-%d')
            batch_to_date = (current_date + delta).strftime('%Y-%m-%d')
            logging.info(f"Fetching news from {batch_from_date} to {batch_to_date}")

            # Fetch news for the given symbol and date range
            news_list = news_fetcher.fetch_news(symbol, from_date=batch_from_date, to_date=batch_to_date)

            # Insert fetched news into the database
            inserted = db_manager.insert_news(symbol, news_list)
            total_articles_added += inserted

            logging.info(f"Inserted {inserted} new articles for {symbol} from {batch_from_date} to {batch_to_date}")

            # Move to the next batch
            current_date += delta

            # Respect API rate limits
            time.sleep(1)  # Sleep for 1 second between API calls

        logging.info(f"Total new articles added to the database: {total_articles_added}")
        logging.info(f"Total articles in the database: {db_manager.get_total_articles()}")

        # Optionally print the news data stored in the database
        if args.print_db:
            db_manager.print_news_data()

    except Exception as e:
        logging.error(f"An error occurred: {e}")

    finally:
        db_manager.close()

if __name__ == '__main__':
    main()
