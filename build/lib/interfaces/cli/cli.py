import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

import argparse
from datetime import datetime
from src.infrastructure.db.stock_repository_impl import StockRepositoryImpl
# Replace the old import
# from src.application.use_cases.create_stock import CreateStock
# Import the consolidated ManageStockUseCase instead
from src.application.use_cases.manage_stock import ManageStockUseCase

def main():
    parser = argparse.ArgumentParser(description="Stock management CLI")
    parser.add_argument('action', choices=['create', 'update', 'delete', 'fetch'])
    parser.add_argument('--ticker', required=True, help="Stock ticker")
    parser.add_argument('--name', help="Stock name")  # No longer required
    parser.add_argument('--industry', help="Industry")  # No longer required
    parser.add_argument('--sector', help="Sector")  # No longer required
    parser.add_argument('--close_price', type=float, help="Close price")
    parser.add_argument('--date', help="Date (YYYY-MM-DD)")  # No longer required

    args = parser.parse_args()

    # Conditionally check for required arguments based on the action
    if args.action == 'create':
        if not all([args.name, args.industry, args.sector, args.close_price, args.date]):
            parser.error("The following arguments are required for 'create': --name, --industry, --sector, --close_price, --date")
    
    repository = StockRepositoryImpl()
    stock_use_case = ManageStockUseCase(stock_repository=repository)

    if args.action == 'create':
        stock_use_case.create_stock(
            ticker=args.ticker,
            name=args.name,
            industry=args.industry,
            sector=args.sector,
            close_price=args.close_price,
            date=args.date
        )
    elif args.action == 'update':
        stock_use_case.update_stock(
            ticker=args.ticker,
            name=args.name,
            industry=args.industry,
            sector=args.sector,
            close_price=args.close_price,
            date=args.date
        )
    elif args.action == 'delete':
        stock_use_case.delete_stock(ticker=args.ticker)
    elif args.action == 'fetch':
        stock = stock_use_case.fetch_stock(ticker=args.ticker)  # Implement if necessary
        print(stock)


if __name__ == "__main__":
    main()
