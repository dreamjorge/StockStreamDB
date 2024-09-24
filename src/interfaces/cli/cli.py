import sys
import os

# Ensure that Python can find the 'src' module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

import argparse
from src.application.use_cases.collect_stock_data import CollectStockData
from src.infrastructure.db.stock_repository import StockRepository
from src.utils.logging_config import setup_logging


def main():
    
    setup_logging()
    parser = argparse.ArgumentParser(
        description="CLI for collecting financial data: stocks, cryptocurrencies, and news"
    )
    parser.add_argument('ticker', help="The stock symbol (e.g., AAPL)")
    parser.add_argument('--period', default="1mo", help="The period to collect data for (e.g., '1d', '1mo')")

    args = parser.parse_args()

    stock_repository = StockRepository()
    use_case = CollectStockData(stock_repository)
    stock = use_case.execute(args.ticker, args.period)

    if stock is None:
        print(f"Error: Could not retrieve data for {args.ticker}.")
    else:
        print(f"Data for {stock.ticker}: Price {stock.close_price}, Date {stock.date}")

if __name__ == "__main__":
    main()
