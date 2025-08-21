from src.containers import Container
from src.domain.models.stock import Stock
from datetime import datetime
import click
import sys
import os

# Add the root directory (the parent of 'src') to the Python path
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)


@click.group()
def cli():
    """Manage stock data."""


@click.command(name="check-data")
@click.argument("ticker")
def check_data(ticker):
    """Print a few stock data entries for a specified ticker."""
    container = Container()
    stock_service = container.stock_service()
    stock = stock_service.fetch_stock(ticker)
    if stock:
        click.echo(
            f"Ticker: {stock.ticker}, "
            f"Date: {stock.date}, "
            f"Close Price: {stock.close}"
        )
    else:
        click.echo(f"No data found for ticker {ticker}")


@click.command()
@click.argument("ticker")
@click.argument("period")
def fetch(ticker, period):
    """Fetch stock data for a specified ticker and period, and log the status."""
    container = Container()
    stock_service = container.stock_service()
    stock_service.fetch_stock(ticker)
    click.echo(f"Fetch complete for {ticker} in the period {period}.")


@click.command()
@click.argument("ticker")
@click.argument("name")
@click.argument("industry")
@click.argument("sector")
@click.argument("close", type=float)
@click.argument("date")
def create(ticker, name, industry, sector, close, date):
    """Create a new stock entry."""
    container = Container()
    stock_service = container.stock_service()
    stock = Stock(
        id=None,
        ticker=ticker,
        name=name,
        industry=industry,
        sector=sector,
        date=datetime.strptime(date, "%Y-%m-%d"),
        close=close,
    )
    stock_service.add_stock(stock)
    click.echo(f"Created stock {ticker}")


@click.command()
@click.argument("ticker")
def delete(ticker):
    """Delete a stock entry."""
    container = Container()
    stock_service = container.stock_service()
    stock_service.remove_stock(ticker)
    click.echo(f"Deleted stock {ticker}")


cli.add_command(check_data)
cli.add_command(fetch)
cli.add_command(create)
cli.add_command(delete)

def main():
    cli()


if __name__ == "__main__":
    main()