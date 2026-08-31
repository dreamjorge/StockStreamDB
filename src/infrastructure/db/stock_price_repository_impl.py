from infrastructure.db.models import StockPrice


class StockPriceRepositoryImpl:
    """Stores and retrieves per-ticker daily OHLCV price history."""

    def __init__(self, session):
        self.session = session

    def save_prices(self, ticker, frame):
        """Upsert a DataFrame with 'date', 'open', 'high', 'low', 'close', 'volume'
        columns (optionally 'adjusted_close') for the given ticker."""
        existing_by_date = {
            record.date: record
            for record in self.session.query(StockPrice).filter_by(ticker=ticker).all()
        }
        for _, row in frame.iterrows():
            observation_date = (
                row["date"].date() if hasattr(row["date"], "date") else row["date"]
            )
            existing = existing_by_date.get(observation_date)
            if existing:
                existing.open = row["open"]
                existing.high = row["high"]
                existing.low = row["low"]
                existing.close = row["close"]
                existing.volume = row["volume"]
                if "adjusted_close" in row:
                    existing.adjusted_close = row["adjusted_close"]
            else:
                new_record = StockPrice(
                    ticker=ticker,
                    date=observation_date,
                    open=row["open"],
                    high=row["high"],
                    low=row["low"],
                    close=row["close"],
                    volume=row["volume"],
                    adjusted_close=(
                        row["adjusted_close"] if "adjusted_close" in row else None
                    ),
                )
                self.session.add(new_record)
                existing_by_date[observation_date] = new_record
        self.session.commit()

    def get_prices(self, ticker):
        """Return all price rows for a ticker, ordered by date."""
        return (
            self.session.query(StockPrice)
            .filter_by(ticker=ticker)
            .order_by(StockPrice.date)
            .all()
        )
