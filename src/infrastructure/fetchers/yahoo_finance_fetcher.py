import yfinance as yf
import pandas as pd


class YahooFinanceFetcher:
    """Fetches stock data from Yahoo Finance."""

    def get_stock_data(self, ticker: str, period: str = "1mo"):
        """Fetches stock data for the given ticker and period.

        Args:
            ticker: The stock ticker.
            period: The period to fetch the data for (e.g., "1mo", "3mo", "1y").

        Returns:
            A dictionary containing the stock data, or None if data could not be fetched.
        """
        try:
            stock = yf.Ticker(ticker)
            stock_data = stock.history(period=period)
        except Exception as e:
            print(f"Network error occurred: {e}")
            return None

        # Return None if data is empty
        if stock_data.empty:
            return None

        stock_data = stock_data.reset_index().rename(columns={"Date": "date"})
        stock_data["date"] = pd.to_datetime(stock_data["date"])
        stock_data.columns = [col.lower() for col in stock_data.columns]

        # Return the last row of data as a dictionary
        last_row = stock_data.iloc[-1]
        return {
            "ticker": ticker,
            "date": last_row["date"].strftime("%Y-%m-%d"),
            "open": last_row["open"],
            "high": last_row["high"],
            "low": last_row["low"],
            "close": last_row["close"],
            "volume": last_row.get("volume", None),
        }
