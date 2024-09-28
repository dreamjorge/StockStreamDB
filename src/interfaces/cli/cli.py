import sys
import os
import argparse
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from src.infrastructure.db.stock_repository_impl import StockRepositoryImpl
from src.application.use_cases.manage_stock import ManageStockUseCase
from src.infrastructure.fetchers.yahoo_finance_fetcher import YahooFinanceFetcher
from src.domain.models.stock import Stock
from src.infrastructure.db.db_setup import session

def add_stock_arguments(parser, include_name=True):
    """Helper function to add common stock arguments."""
    parser.add_argument("ticker")
    if include_name:
        parser.add_argument("name")
        parser.add_argument("industry")
        parser.add_argument("sector")
        parser.add_argument("close_price", type=float)
        parser.add_argument("date")

def parse_date(date_string):
    """Helper function to parse date from string."""
    return datetime.strptime(date_string, "%Y-%m-%d").date()

def create_stock_from_args(args):
    """Helper function to create a Stock object from parsed arguments."""
    stock_date = parse_date(args.date)
    return Stock(
        ticker=args.ticker,
        name=args.name,
        industry=args.industry,
        sector=args.sector,
        close_price=args.close_price,
        date=stock_date
    )

def execute_create(args, stock_use_case):
    stock = create_stock_from_args(args)
    stock_use_case.create_stock(stock)
    print(f"Created stock {stock.ticker}")

def execute_update(args, stock_use_case):
    stock = create_stock_from_args(args)
    updated_stock = stock_use_case.update_stock(stock)
    if updated_stock:
        print(f"Updated stock {updated_stock.ticker}")
    else:
        print(f"Stock with ticker {args.ticker} not found for update.")

def execute_get(args, stock_use_case):
    stock = stock_use_case.get_stock(args.ticker)  # Corrected method name
    if stock:
        print(f"Stock: {stock.name}, Industry: {stock.industry}, Sector: {stock.sector}")
    else:
        print(f"Stock with ticker {args.ticker} not found.")

def execute_delete(args, stock_use_case):
    result = stock_use_case.delete_stock(args.ticker)
    if result:
        print(f"Deleted stock {args.ticker}")
    else:
        print(f"Stock with ticker {args.ticker} not found.")

def execute_fetch(args):
    yahoo_finance_fetcher = YahooFinanceFetcher()
    stock_data = yahoo_finance_fetcher.fetch(args.ticker, args.period)
    if stock_data:
        print(f"Fetched stock: {stock_data['name']}, Close Price: {stock_data['close_price']}, Date: {stock_data['date']}")
    else:
        print(f"No data found for {args.ticker} in the period '{args.period}'.")

def main():
    parser = argparse.ArgumentParser(description="Manage stock data")
    subparsers = parser.add_subparsers(dest="command")

    # Create command
    create_parser = subparsers.add_parser("create")
    add_stock_arguments(create_parser)

    # Get command
    get_parser = subparsers.add_parser("get")
    get_parser.add_argument("ticker")

    # Update command
    update_parser = subparsers.add_parser("update")
    add_stock_arguments(update_parser)

    # Delete command
    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("ticker")

    # Fetch stock data
    fetch_parser = subparsers.add_parser("fetch")
    fetch_parser.add_argument("ticker")
    fetch_parser.add_argument("period", help="e.g. 1d, 1mo, 6mo, 1y")

    args = parser.parse_args()

    stock_repo = StockRepositoryImpl(session)
    stock_use_case = ManageStockUseCase(stock_repo)

    if args.command == "create":
        execute_create(args, stock_use_case)
    elif args.command == "get":
        execute_get(args, stock_use_case)
    elif args.command == "update":
        execute_update(args, stock_use_case)
    elif args.command == "delete":
        execute_delete(args, stock_use_case)
    elif args.command == "fetch":
        execute_fetch(args)

if __name__ == "__main__":
    main()
