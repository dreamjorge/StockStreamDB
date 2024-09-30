# src/infrastructure/fetchers/yahoo_finance_fetcher.py

import yfinance as yf
from src.repositories.stock_fetcher import StockFetcher

class YahooFinanceFetcher(StockFetcher):

    def fetch(self, ticker: str, period: str):
        # Use yfinance to fetch data
        stock_data = yf.Ticker(ticker).history(period=period)
        
        if stock_data.empty:
            return None
        
        # Return the most recent stock data as a dictionary
        return {
            'ticker': ticker,
            'close_price': stock_data['Close'].iloc[-1],
            'date': stock_data.index[-1].strftime('%Y-%m-%d'),
            'open': stock_data['Open'].iloc[-1],
            'high': stock_data['High'].iloc[-1],
            'low': stock_data['Low'].iloc[-1],
            'volume': stock_data['Volume'].iloc[-1],
        }
