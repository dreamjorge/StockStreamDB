class ManageMacroUseCase:
    """Fetch-and-store orchestration for FRED macro indicators."""

    def __init__(self, macro_repo, macro_fetcher=None):
        self.macro_repo = macro_repo
        self.macro_fetcher = macro_fetcher

    def fetch_and_store_series(self, series_id, start=None, end=None):
        """Fetch a FRED series and upsert it into the database. Returns the number of
        observations stored, or 0 if the fetcher returned no data."""
        if not self.macro_fetcher:
            raise ValueError("MacroFetcher not provided.")

        frame = self.macro_fetcher.fetch(series_id, start=start, end=end)
        if frame is None or frame.empty:
            return 0

        self.macro_repo.save_series(series_id, frame)
        return len(frame)

    def series_exists(self, series_id):
        return self.macro_repo.series_exists(series_id)
