# src/application/generate_stock_data.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Helper function to generate random stock prices


def generate_stock_data(ticker, start_date, end_date):
    num_days = (end_date - start_date).days
    dates = pd.date_range(start=start_date, end=end_date - timedelta(days=1), freq="D")
    prices = (
        np.cumsum(np.random.normal(loc=0.5, scale=1.0, size=num_days)) + 100
    )  # Random walk
    return pd.DataFrame({"date": dates, "ticker": ticker, "price": prices})


def save_stock_data_to_csv(tickers, start_date, end_date, output_file):
    all_data = pd.concat(
        [generate_stock_data(ticker, start_date, end_date) for ticker in tickers],
        ignore_index=True,
    )
    all_data.to_csv(output_file, index=False)


if __name__ == "__main__":
    tickers = ["NVDA", "AAPL", "MSFT"]
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 1, 1)
    output_file = "stock_data.csv"  # Adjust the path as needed

    save_stock_data_to_csv(tickers, start_date, end_date, output_file)
    print(f"Stock data saved to {output_file}")
