import click
from datetime import datetime
from src.infrastructure.db.stock_repository_impl import StockRepositoryImpl
from src.application.use_cases.manage_stock import ManageStockUseCase  # Correct import
from src.infrastructure.db.db_setup import get_session
from src.infrastructure.fetchers.yahoo_finance_fetcher import YahooFinanceFetcher

@click.group()
def cli():
    """Manage stock data."""
    pass

@click.command()
@click.argument('ticker')
def check_data(ticker):
    """Print a few stock data entries for a specified ticker."""
    with get_session() as session:
        stock_repo = StockRepositoryImpl(session)
        data = stock_repo.get_sample_stock_data(ticker)
        if data:
            for stock in data:
                click.echo(f"Ticker: {stock.ticker}, Date: {stock.date}, Close Price: {stock.close}")
        else:
            click.echo(f"No data found for ticker {ticker}")



@click.command()
@click.argument('ticker')
@click.argument('period')
def fetch(ticker, period):
    """Fetch stock data for a specified ticker and period, and log the status."""
    with get_session() as session:
        stock_repo = StockRepositoryImpl(session)
        stock_fetcher = YahooFinanceFetcher()  # Initialize the stock fetcher
        stock_use_case = ManageStockUseCase(stock_repo, stock_fetcher)  # Pass the stock fetcher
        
        # Check if the stock data already exists in the database
        existing_data = stock_use_case.check_stock_exists(ticker, period)
        
        if existing_data:
            click.echo(f"Data for {ticker} in the period {period} already exists.")
        else:
            stock_use_case.fetch_stock_data(ticker, period)
            click.echo(f"Fetch complete for {ticker} in the period {period}.")


@click.command()
@click.argument('ticker')
@click.argument('name')
@click.argument('industry')
@click.argument('sector')
@click.argument('close_price', type=float)
@click.argument('date')
def create(ticker, name, industry, sector, close_price, date):
    """Create a new stock entry."""
    # Validate ticker format
    if not ticker.isalpha() or len(ticker) > 5:
        raise click.ClickException("Error: Invalid ticker format.")
    
    # Validate date format
    try:
        stock_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise click.ClickException("Error: Invalid value for 'DATE'. Must be in YYYY-MM-DD format.")
    
    # Use a session to interact with the database
    with get_session() as session:
        stock_repo = StockRepositoryImpl(session)
        stock_use_case = ManageStockUseCase(stock_repo)
        
        # Create the stock
        stock_use_case.create_stock(
            ticker=ticker, 
            name=name, 
            industry=industry, 
            sector=sector, 
            close_price=close_price, 
            date=stock_date
        )
        click.echo(f"Created stock {ticker}")


@click.command()
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
            raise click.ClickException(f"Stock with ticker {ticker} not found.")  # Raise a ClickException here
        
# Register commands only once
cli.add_command(create)
cli.add_command(fetch)
cli.add_command(delete)
cli.add_command(check_data)

def main():
    cli()

if __name__ == "__main__":
    main()

