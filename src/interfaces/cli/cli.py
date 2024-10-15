from utils.stock_plotting import plot_stock_prices
from application.generate_stock_data import save_stock_data_to_csv
from infrastructure.fetchers.yahoo_finance_fetcher import YahooFinanceFetcher
from infrastructure.db.db_setup import get_session
from application.use_cases.manage_stock import ManageStockUseCase
from infrastructure.db.stock_repository_impl import StockRepositoryImpl
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


# Command to check data


# Command to check data
@click.command(name="check-data")  # Hyphenated name for CLI
@click.argument("ticker")
def check_data(ticker):
    """Print a few stock data entries for a specified ticker."""
    with get_session() as session:
        stock_repo = StockRepositoryImpl(session)
        data = stock_repo.get_sample_stock_data(ticker)
        if data:
            for stock in data:
                click.echo(
                    f"Ticker: {stock.ticker}, "
                    f"Date: {stock.date}, "
                    f"Close Price: {stock.close}"
                )
        else:
            click.echo(f"No data found for ticker {ticker}")


# Command to fetch stock data


@click.command()
@click.argument("ticker")
@click.argument("period")
def fetch(ticker, period):
    """Fetch stock data for a specified ticker and period, and log the status."""
    with get_session() as session:
        stock_repo = StockRepositoryImpl(session)
        stock_fetcher = YahooFinanceFetcher()
        stock_use_case = ManageStockUseCase(stock_repo, stock_fetcher)

        # Check if the stock data already exists in the database
        existing_data = stock_use_case.check_stock_exists(ticker, period)
        if existing_data:
            click.echo(f"Data for {ticker} in the period {period} already exists.")
        else:
            stock_use_case.fetch_stock_data(ticker, period)
            click.echo(f"Fetch complete for {ticker} in the period {period}.")


# Command to create a new stock entry


@click.command()
@click.argument("ticker")
@click.argument("name")
@click.argument("industry")
@click.argument("sector")
@click.argument("close", type=float)
@click.argument("date")
def create(ticker, name, industry, sector, close, date, stock_fetcher=None):
    """Create a new stock entry."""
    if not ticker.isalpha() or len(ticker) > 5:
        raise click.ClickException("Error: Invalid ticker format.")
    try:
        stock_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise click.ClickException(
            "Error: Invalid value for 'DATE'. Must be in YYYY-MM-DD format."
        )

    with get_session() as session:
        stock_repo = StockRepositoryImpl(session)
        if stock_fetcher is None:
            stock_fetcher = YahooFinanceFetcher()
        stock_use_case = ManageStockUseCase(stock_repo, stock_fetcher)
        stock_use_case.create_stock(
            ticker=ticker,
            name=name,
            industry=industry,
            sector=sector,
            close=close,
            date=stock_date,
        )
        click.echo(f"Created stock {ticker}")


@click.command()
@click.argument("ticker")
def delete(ticker):
    """Delete a stock entry."""
    with get_session() as session:
        stock_repo = StockRepositoryImpl(session)
        stock_use_case = ManageStockUseCase(stock_repo)  # No need to pass stock_fetcher
        result = stock_use_case.delete_stock(ticker)
        if result:
            click.echo(f"Deleted stock {ticker}")
        else:
            raise click.ClickException(f"Stock with ticker {ticker} not found.")


# Command to generate stock data (NVIDIA, Apple, Microsoft)


@click.command()
@click.option(
    "--tickers", default="NVDA,AAPL,MSFT", help="Comma-separated list of tickers."
)
@click.option(
    "--start-date", default="2023-01-01", help="Start date for stock data generation."
)
@click.option(
    "--end-date", default="2024-01-01", help="End date for stock data generation."
)
@click.option(
    "--output-file",
    default="stock_data.csv",
    help="CSV file to store generated stock data.",
)
def generate_data(tickers, start_date, end_date, output_file):
    """Generate stock price data for the specified tickers."""
    tickers_list = tickers.split(",")
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    save_stock_data_to_csv(tickers_list, start, end, output_file)
    click.echo(f"Generated stock data for {tickers} and saved to {output_file}")


# Command to plot stock data


@click.command(name="plot-data")  # Hyphenated name for CLI
@click.option("--csv-file", default="stock_data.csv", help="CSV file with stock data.")
@click.option("--ticker", default="NVDA", help="Ticker symbol to plot.")
def plot_data(csv_file, ticker):
    """Plot stock price data for the specified ticker."""
    plot_stock_prices(csv_file, ticker)
    click.echo(f"Plotted stock prices for {ticker}")


# Register commands
cli.add_command(check_data)
cli.add_command(fetch)
cli.add_command(create)
cli.add_command(delete)
cli.add_command(generate_data)
cli.add_command(plot_data)


def main():
    cli()


if __name__ == "__main__":
    main()
