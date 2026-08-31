from infrastructure.db.models import MacroIndicator


class MacroRepositoryImpl:
    """Stores and retrieves FRED macro-indicator observations."""

    def __init__(self, session):
        self.session = session

    def save_series(self, series_id, frame):
        """Upsert a DataFrame with 'date' and 'value' columns for the given series_id."""
        existing_by_date = {
            record.date: record
            for record in self.session.query(MacroIndicator)
            .filter_by(series_id=series_id)
            .all()
        }
        for _, row in frame.iterrows():
            observation_date = (
                row["date"].date() if hasattr(row["date"], "date") else row["date"]
            )
            existing = existing_by_date.get(observation_date)
            if existing:
                existing.value = row["value"]
            else:
                self.session.add(
                    MacroIndicator(
                        series_id=series_id, date=observation_date, value=row["value"]
                    )
                )
        self.session.commit()

    def get_series(self, series_id):
        """Return all observations for a series, ordered by date."""
        return (
            self.session.query(MacroIndicator)
            .filter_by(series_id=series_id)
            .order_by(MacroIndicator.date)
            .all()
        )

    def series_exists(self, series_id):
        """Return True if any observation exists for the given series_id."""
        return self.session.query(
            self.session.query(MacroIndicator).filter_by(series_id=series_id).exists()
        ).scalar()
