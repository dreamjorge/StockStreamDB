import click
from datetime import datetime
from src.infrastructure.db.stock_repository_impl import StockRepositoryImpl
from src.application.use_cases.manage_stock import ManageStockUseCase  # Correct import
from src.infrastructure.db.db_setup import get_session

@click.group()
def cli():
    """Manage stock data."""
    pass

@click.command()
@click.argument('ticker')
@click.argument('name')
@click.argument('industry')
@click.argument('sector')
@click.argument('close_price', type=float)
@click.argument('date')
def create(ticker, name, industry, sector, close_price, date):
    """Create a new stock entry."""
    try:
        stock_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise click.ClickException("Error: Invalid value for 'DATE'. Must be in YYYY-MM-DD format.")
    
    with get_session() as session:
        stock_repo = StockRepositoryImpl(session)
        stock_use_case = ManageStockUseCase(stock_repo)
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
@click.argument('period')
def fetch(ticker, period):
    """Fetch stock data for a specified ticker and period."""
    with get_session() as session:
        stock_repo = StockRepositoryImpl(session)
        stock_use_case = ManageStockUseCase(stock_repo)
        data = stock_use_case.fetch_stock_data(ticker, period)
        if not data.empty:
            click.echo(data.to_string(index=False))
        else:
            click.echo(f"No data found for ticker {ticker} in the period {period}.")

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

def main():
    cli()

if __name__ == "__main__":
    main()

