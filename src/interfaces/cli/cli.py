# src/interfaces/cli/cli.py

import sys
import os
from datetime import datetime
import click

# Adjust the system path to include the project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from src.infrastructure.db.stock_repository_impl import StockRepositoryImpl
from src.application.use_cases.manage_stock import ManageStockUseCase
from src.infrastructure.fetchers.yahoo_finance_fetcher import YahooFinanceFetcher
from src.domain.models.stock import Stock
from src.infrastructure.db.db_setup import get_session
from interfaces.common.enums import Granularity
from src.repositories.concrete_stocks_repository import ConcreteStocksRepository
from src.application.use_cases.fetch_and_store_stock_use_case import FetchAndStoreStockUseCase

@click.group()
def cli():
    """Manage stock data."""
    pass

@cli.command()
@click.argument('ticker')
@click.argument('name')
@click.argument('industry')
@click.argument('sector')
@click.argument('close_price', type=float)
@click.argument('date')
def create(ticker, name, industry, sector, close_price, date):
    """Create a new stock entry."""
    with get_session() as session:
        stock_repo = StockRepositoryImpl(session)
        stock_use_case = ManageStockUseCase(stock_repo)
        stock = Stock(
            ticker=ticker,
            name=name,
            industry=industry,
            sector=sector,
            close_price=close_price,
            date=datetime.strptime(date, "%Y-%m-%d").date()
        )
        stock_use_case.create_stock(stock)
        click.echo(f"Created stock {ticker}")

@cli.command()
@click.argument('ticker')
def get(ticker):
    """Get stock information."""
    with get_session() as session:
        stock_repo = StockRepositoryImpl(session)
        stock_use_case = ManageStockUseCase(stock_repo)
        stock = stock_use_case.get_stock(ticker)
        if stock:
            click.echo(f"Stock: {stock.name}, Industry: {stock.industry}, Sector: {stock.sector}")
        else:
            click.echo(f"Stock with ticker {ticker} not found.")

@cli.command()
@click.argument('ticker')
@click.argument('name')
@click.argument('industry')
@click.argument('sector')
@click.argument('close_price', type=float)
@click.argument('date')
def update(ticker, name, industry, sector, close_price, date):
    """Update an existing stock entry."""
    with get_session() as session:
        stock_repo = StockRepositoryImpl(session)
        stock_use_case = ManageStockUseCase(stock_repo)
        stock = Stock(
            ticker=ticker,
            name=name,
            industry=industry,
            sector=sector,
            close_price=close_price,
            date=datetime.strptime(date, "%Y-%m-%d").date()
        )
        updated_stock = stock_use_case.update_stock(stock)
        if updated_stock:
            click.echo(f"Updated stock {ticker}")
        else:
            click.echo(f"Stock with ticker {ticker} not found for update.")

@cli.command()
@click.argument('ticker')
def delete(ticker):
    """Delete a stock entry."""
    with get_session() as session:
        stock_repo = StockRepositoryImpl(session)
        stock_use_case = ManageStockUseCase(stock_repo)
        result = stock_use_case.delete_stock(ticker)
        if result:
            click.echo(f"Deleted stock {ticker}")
        else:
            click.echo(f"Stock with ticker {ticker} not found.")

@cli.command()
@click.argument('ticker')
@click.argument('period')
def fetch(ticker, period):
    """Fetch stock data for a specified ticker and period."""
    with get_session() as session:
        stock_repo = StockRepositoryImpl(session)
        stock_use_case = ManageStockUseCase(stock_repo)
        try:
            data = stock_use_case.fetch_stock_data(ticker, period)
            if data:
                click.echo(data.to_string(index=False))
            else:
                click.echo(f"No data found for ticker {ticker} in the period {period}.")
        except Exception as e:
            click.echo(f"An error occurred while fetching data: {e}")

def main():
    cli()

if __name__ == "__main__":
    main()
