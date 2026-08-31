import yfinance as yf
import pandas as pd

# yfinance's period argument uses "1mo" for one month; "1m" is reserved there for a
# one-minute *interval*. The application layer (ManageStockUseCase, StockRepositoryImpl)
# accepts "1m" as a period synonym for "1mo", so normalize it here before calling
# yfinance, otherwise "1m" is silently treated as an invalid period.
_YFINANCE_PERIOD_ALIASES = {"1m": "1mo"}


class YahooFinanceFetcher:
    def fetch(self, ticker, period="1mo", return_format="dataframe"):
        resolved_period = _YFINANCE_PERIOD_ALIASES.get(period, period)
        try:
            stock = yf.Ticker(ticker)
            stock_data = stock.history(period=resolved_period)
        except Exception as e:
            print(f"Network error occurred: {e}")
            return None

        # Return None if data is empty
        if stock_data.empty:
            return None

        stock_data = stock_data.reset_index().rename(columns={"Date": "date"})
        stock_data["date"] = pd.to_datetime(stock_data["date"])
        stock_data.columns = [col.lower() for col in stock_data.columns]

        # Handle different return formats
        if return_format == "dataframe":
            return stock_data[["date", "open", "high", "low", "close", "volume"]]
        elif return_format == "list":
            return [
                {
                    "ticker": ticker,
                    "date": row["date"].strftime("%Y-%m-%d"),
                    "open": row["open"],
                    "high": row["high"],
                    "low": row["low"],
                    "close": row["close"],
                    "volume": row.get("volume", None),
                }
                for _, row in stock_data.iterrows()
            ]
        elif return_format == "dict":
            return {
                row["date"].strftime("%Y-%m-%d"): {
                    "ticker": ticker,
                    "open": row["open"],
                    "high": row["high"],
                    "low": row["low"],
                    "close": row["close"],
                    "volume": row.get("volume", None),
                }
                for _, row in stock_data.iterrows()
            }
        else:
            raise ValueError("Unsupported return_format")
