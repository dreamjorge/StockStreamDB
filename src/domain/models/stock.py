from dataclasses import dataclass
from datetime import datetime


@dataclass
class Stock:
    id: int
    ticker: str
    name: str
    industry: str
    sector: str
    date: datetime
    open: float | None = None
    high: float | None = None
    low: float | None = None
    close: float | None = None
    volume: float | None = None
    market_cap: float | None = None
    pe_ratio: float | None = None