import time
import yfinance as yf
import requests
from requests.exceptions import RequestException

class StockRepository:
    def get_stock_data(self, ticker: str, period: str = '1mo', retries: int = 3):
        attempt = 0
        while attempt < retries:
            try:
                # Attempt to fetch the data
                stock_data = yf.Ticker(ticker).history(period=period)

                # Check if the data is empty
                if stock_data.empty:
                    return None

                # Return the data if available
                return {'close': stock_data['Close'].iloc[-1], 'date': str(stock_data.index[-1])}
            
            except RequestException as e:
                print(f"Connection error while attempting to fetch data for {ticker}. Retrying ({attempt+1}/{retries})...")
                attempt += 1
                time.sleep(2)  # Wait for 2 seconds before retrying

            except Exception as e:
                print(f"Error processing data for {ticker}: {e}")
                return None

        print(f"Connection error: Failed to retrieve data for {ticker} after {retries} attempts.")
        return None
