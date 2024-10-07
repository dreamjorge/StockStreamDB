import time
import yfinance as yf
from requests.exceptions import RequestException


class StockRepository:
    def get_stock_data(self, ticker: str, period: str = "1mo", retries: int = 3):
        attempt = 0
        while attempt < retries:
            try:
                # Attempt to fetch the data
                stock_data = yf.Ticker(ticker).history(period=period)

                # Check if the data is empty
                if stock_data.empty:
                    return None

                # Format the date to 'YYYY-MM-DD'
                close = stock_data["Close"].iloc[-1]
                date = stock_data.index[-1].strftime("%Y-%m-%d")

                # Return the close price and date
                return {"close": close, "date": date}

            except RequestException as e:
                print(
                    f"Connection error while attempting to fetch data for \
                        {ticker}. Retrying ({attempt + 1}/{retries})..."
                )
                print(e)
                attempt += 1
                time.sleep(2)  # Wait for 2 seconds before retrying

            except ValueError as e:
                print(f"Data parsing error for {ticker}: {e}")
                print(e)
                return None

            except Exception as e:
                print(f"Unexpected error for {ticker}: {e}")
                print(e)
                return None

        print(
            f"Connection error: Failed to retrieve data \
                for {ticker} after {retries} attempts."
        )
        return None
