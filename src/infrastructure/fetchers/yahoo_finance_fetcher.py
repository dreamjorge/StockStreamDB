# src/infrastructure/fetchers/yahoo_finance_fetcher.py

import yfinance as yf
from src.repositories.stock_fetcher import StockFetcher

class YahooFinanceFetcher:
    def fetch(self, ticker: str, period: str):
        stock_data = yf.Ticker(ticker).history(period=period, interval="1d")
        if stock_data.empty:
            return []

        # Convert stock data to a list of dictionaries
        return [
            {
                'ticker': ticker,
                'close_price': row['Close'],
                'date': index.strftime('%Y-%m-%d'),
                'open': row['Open'],
                'high': row['High'],
                'low': row['Low'],
                'volume': row['Volume']
            }
            for index, row in stock_data.iterrows()
        ]