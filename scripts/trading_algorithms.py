import yfinance as yf
import pandas as pd


def fetch_stock_data(ticker: str, period: str = "1y") -> pd.DataFrame:
    """Fetch historical data for the ticker using yfinance."""
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    if data.empty:
        raise ValueError(f"No data found for ticker {ticker}")
    data = data.reset_index().rename(columns={"Date": "date"})
    return data


def simple_moving_average(data: pd.Series, window: int = 20) -> pd.Series:
    """Calculate the Simple Moving Average (SMA)."""
    return data.rolling(window=window).mean()


def exponential_moving_average(data: pd.Series, window: int = 20) -> pd.Series:
    """Calculate the Exponential Moving Average (EMA)."""
    return data.ewm(span=window, adjust=False).mean()


def rsi(data: pd.Series, window: int = 14) -> pd.Series:
    """Calculate the Relative Strength Index (RSI)."""
    delta = data.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def z_score(data: pd.Series, window: int = 50) -> pd.Series:
    """Calculate the z-score of the price relative to a moving average."""
    mean = data.rolling(window=window).mean()
    std = data.rolling(window=window).std()
    return (data - mean) / std


def generate_signals(df: pd.DataFrame) -> pd.DataFrame:
    """Generate basic trading signals using SMA crossover and RSI."""
    df = df.copy()
    df["SMA_20"] = simple_moving_average(df["Close"], 20)
    df["SMA_50"] = simple_moving_average(df["Close"], 50)
    df["RSI"] = rsi(df["Close"], 14)

    df["Signal"] = 0
    df.loc[df["SMA_20"] > df["SMA_50"], "Signal"] = 1
    df.loc[df["SMA_20"] < df["SMA_50"], "Signal"] = -1
    return df


def generate_simons_signals(df: pd.DataFrame) -> pd.DataFrame:
    """Generate trading signals inspired by quantitative strategies."""
    df = df.copy()
    df["EMA_20"] = exponential_moving_average(df["Close"], 20)
    df["EMA_50"] = exponential_moving_average(df["Close"], 50)
    df["Z_50"] = z_score(df["Close"], 50)

    df["Signal"] = 0
    buy = (df["EMA_20"] > df["EMA_50"]) & (df["Z_50"] > 1)
    sell = (df["EMA_20"] < df["EMA_50"]) & (df["Z_50"] < -1)
    df.loc[buy, "Signal"] = 1
    df.loc[sell, "Signal"] = -1
    return df


def main(ticker: str, period: str = "1y", strategy: str = "basic"):
    """Run the selected trading strategy."""
    df = fetch_stock_data(ticker, period)
    if strategy == "simons":
        df = generate_simons_signals(df)
        cols = ["date", "Close", "EMA_20", "EMA_50", "Z_50", "Signal"]
    else:
        df = generate_signals(df)
        cols = ["date", "Close", "SMA_20", "SMA_50", "RSI", "Signal"]
    print(df[cols].tail())


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run sample trading algorithms")
    parser.add_argument("ticker", help="Ticker symbol, e.g., AAPL")
    parser.add_argument(
        "--period", default="1y", help="Data period to fetch from yfinance"
    )
    parser.add_argument(
        "--strategy",
        choices=["basic", "simons"],
        default="basic",
        help="Trading strategy to use",
    )
    args = parser.parse_args()

    main(args.ticker, period=args.period, strategy=args.strategy)
