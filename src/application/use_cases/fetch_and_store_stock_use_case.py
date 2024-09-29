from src.infrastructure.fetchers.yahoo_finance_fetcher import YahooFinanceFetcher
from src.infrastructure.db.stock_repository_impl import StockRepositoryImpl
from src.domain.models.stock import Stock

class FetchAndStoreStockUseCase:
    def __init__(self, yahoo_finance_fetcher, stock_repository):
        self.yahoo_finance_fetcher = yahoo_finance_fetcher
        self.stock_repository = stock_repository

    def execute(self, ticker: str, period: str = '1mo'):
        # Fetch data from Yahoo Finance
        stock_data = self.yahoo_finance_fetcher.fetch(ticker, period)
        
        # Loop through each row and save the stock data
        for index, row in stock_data.iterrows():
            stock = Stock(
                ticker=ticker,
                name="N/A",  # You can add logic to retrieve the stock name if needed
                industry="N/A",  # You can add logic to retrieve the industry if needed
                sector="N/A",  # You can add logic to retrieve the sector if needed
                close_price=row['Close'],
                date=index,
                open=row['Open'],
                high=row['High'],
                low=row['Low'],
                close=row['Close'],
                volume=row['Volume']
            )
            self.stock_repository.save(stock)