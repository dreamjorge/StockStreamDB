import sys
import os
import argparse
from sqlalchemy.orm import sessionmaker
from src.infrastructure.db.db_setup import engine
from src.application.use_cases.manage_stock import CreateStock, GetStock, UpdateStock, DeleteStock
from src.infrastructure.db.stock_repository_impl import StockRepositoryImpl
from src.domain.models.stock import Stock
from datetime import datetime

# Add the project's root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

Session = sessionmaker(bind=engine)
session = Session()

def main():
    parser = argparse.ArgumentParser(description="Manage stock data")
    subparsers = parser.add_subparsers(dest="command")

    # Create
    create_parser = subparsers.add_parser("create")
    create_parser.add_argument("ticker")
    create_parser.add_argument("name")
    create_parser.add_argument("industry")
    create_parser.add_argument("sector")
    create_parser.add_argument("close_price", type=float)
    create_parser.add_argument("date")

    # Get
    get_parser = subparsers.add_parser("get")
    get_parser.add_argument("ticker")

    # Update
    update_parser = subparsers.add_parser("update")
    update_parser.add_argument("ticker")
    update_parser.add_argument("name")
    update_parser.add_argument("industry")
    update_parser.add_argument("sector")
    update_parser.add_argument("close_price", type=float)
    update_parser.add_argument("date")

    # Delete
    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("ticker")

    args = parser.parse_args()

    stock_repo = StockRepositoryImpl(session)

    if args.command == "create":
        stock_date = datetime.strptime(args.date, "%Y-%m-%d").date()  # Convert string to date
        stock = Stock(
            ticker=args.ticker,
            name=args.name,
            industry=args.industry,
            sector=args.sector,
            close_price=args.close_price,
            date=stock_date
        )
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
        stock_date = datetime.strptime(args.date, "%Y-%m-%d").date()  # Convert string to date
        stock = Stock(
            ticker=args.ticker,
            name=args.name,
            industry=args.industry,
            sector=args.sector,
            close_price=args.close_price,
            date=stock_date
        )
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

if __name__ == "__main__":
    main()
