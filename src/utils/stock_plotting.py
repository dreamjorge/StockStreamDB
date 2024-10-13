# src/utils/stock_plotting.py
import pandas as pd
import plotly.express as px


def plot_stock_prices(csv_file, ticker):
    stock_data = pd.read_csv(csv_file)
    stock_data = stock_data[stock_data["ticker"] == ticker]

    # Create an interactive line plot
    fig = px.line(
        stock_data,
        x="date",
        y="price",
        title=f"{ticker} Stock Prices (1 Year)",
        labels={"date": "Date", "price": "Price"},
    )

    fig.update_layout(xaxis_title="Date", yaxis_title="Price", template="plotly_dark")

    # Show the interactive plot
    fig.show()


if __name__ == "__main__":
    csv_file = "stock_data.csv"  # Adjust the path as needed
    ticker = "NVDA"  # You can change this to "AAPL" or "MSFT"

    plot_stock_prices(csv_file, ticker)
