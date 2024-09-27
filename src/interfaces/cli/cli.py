import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

import argparse
from datetime import datetime
from src.infrastructure.db.stock_repository_impl import StockRepositoryImpl
from src.application.use_cases.create_stock import CreateStock
from src.application.use_cases.get_stock import GetStock
from src.application.use_cases.update_stock import UpdateStock
from src.application.use_cases.delete_stock import DeleteStock
from src.application.use_cases.collect_stock_data import CollectStockData
from src.infrastructure.fetchers.yahoo_finance_fetcher import YahooFinanceFetcher  # Import the fetcher
from src.domain.models.stock import Stock
from src.infrastructure.db.db_setup import session

def add_stock_arguments(parser):
    parser.add_argument("ticker")
    parser.add_argument("name")
    parser.add_argument("industry")
    parser.add_argument("sector")
    parser.add_argument("close_price", type=float)
    parser.add_argument("date")

def create_stock_from_args(args):
    stock_date = datetime.strptime(args.date, "%Y-%m-%d").date()  # Convert string to date
    stock = Stock(
        ticker=args.ticker,
        name=args.name,
        industry=args.industry,
        sector=args.sector,
        close_price=args.close_price,
        date=stock_date
    )
    return stock

def main():
    parser = argparse.ArgumentParser(description="Manage stock data")
    subparsers = parser.add_subparsers(dest="command")

    # Create
    create_parser = subparsers.add_parser("create")
    add_stock_arguments(create_parser)

    # Get
    get_parser = subparsers.add_parser("get")
    get_parser.add_argument("ticker")

    # Update
    update_parser = subparsers.add_parser("update")
    add_stock_arguments(update_parser)

    # Delete
    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("ticker")

    # Collect Stock Data from External Source
    fetch_parser = subparsers.add_parser("fetch")
    fetch_parser.add_argument("ticker")
    fetch_parser.add_argument("period", help="e.g. 1d, 1mo, 6mo, 1y")

    args = parser.parse_args()

    stock_repo = StockRepositoryImpl(session)

    if args.command == "create":
        stock = create_stock_from_args(args)
        use_case = CreateStock(stock_repo)
        use_case.execute(stock)
        print(f"Created stock {stock.ticker}")

    elif args.command == "get":
        use_case = GetStock(stock_repo)
        stock = use_case.execute(args.ticker)
        if stock:
            print(f"Stock: {stock.name}, Industry: {stock.industry}, Sector: {stock.sector}")
        else:
            print(f"Stock with ticker {args.ticker} not found.")

    elif args.command == "update":
        stock = create_stock_from_args(args)
        use_case = UpdateStock(stock_repo)
        updated_stock = use_case.execute(stock)
        if updated_stock:
            print(f"Updated stock {updated_stock.ticker}")
        else:
            print(f"Stock with ticker {args.ticker} not found for update.")

    elif args.command == "delete":
        use_case = DeleteStock(stock_repo)
        result = use_case.execute(args.ticker)
        if result:
            print(f"Deleted stock {args.ticker}")
        else:
            print(f"Stock with ticker {args.ticker} not found.")

    elif args.command == "fetch":
        # Inject the YahooFinanceFetcher into CollectStockData use case
        yahoo_finance_fetcher = YahooFinanceFetcher()
        collect_stock_data = CollectStockData(yahoo_finance_fetcher)

        # Fetch data for the specified ticker and period
        stock = collect_stock_data.execute(args.ticker, args.period)
        if stock:
            print(f"Fetched stock: {stock.name}, Close Price: {stock.close_price}, Date: {stock.date}")
        else:
            print(f"No data found for {args.ticker} in the period '{args.period}'.")

if __name__ == "__main__":
    main()
