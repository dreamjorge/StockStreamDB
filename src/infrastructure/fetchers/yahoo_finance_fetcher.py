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
