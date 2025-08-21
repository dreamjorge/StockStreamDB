from dataclasses import dataclass
from datetime import datetime


@dataclass
class Stock:
    """Domain model for a stock."""

    id: int
    """The unique identifier of the stock."""

    ticker: str
    """The stock ticker."""

    name: str
    """The name of the stock."""

    industry: str
    """The industry the stock belongs to."""

    sector: str
    """The sector the stock belongs to."""

    date: datetime
    """The date of the stock data."""

    open: float | None = None
    """The opening price of the stock."""

    high: float | None = None
    """The highest price of the stock."""

    low: float | None = None
    """The lowest price of the stock."""

    close: float | None = None
    """The closing price of the stock."""

    volume: float | None = None
    """The volume of the stock traded."""

    market_cap: float | None = None
    """The market capitalization of the stock."""

    pe_ratio: float | None = None
    """The price-to-earnings ratio of the stock."""
