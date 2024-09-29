import yfinance as yf
from src.domain.stock_fetcher import StockFetcher

class YahooFinanceFetcher(StockFetcher):
    def get_stock_data(self, ticker: str, period: str) -> dict:
        stock = yf.Ticker(ticker)
        history = stock.history(period=period)

        if history.empty:
            return None
        
        # Extract required fields from the history
        return {
            'ticker': ticker,
            'name': stock.info.get('longName'),
            'industry': stock.info.get('industry'),
            'sector': stock.info.get('sector'),
            'close': history['Close'].iloc[-1],
            'date': history.index[-1]
        }

    def fetch(self, ticker: str, period: str = '1mo'):
        """
        Fetch stock data from Yahoo Finance for a given ticker and period.

        :param ticker: Stock ticker (e.g., 'AAPL')
        :param period: Time period (e.g., '1d', '1mo', '6mo', '1y')
        :return: DataFrame containing stock data
        """
        stock = yf.Ticker(ticker)
        stock_data = stock.history(period=period)
        return stock_data