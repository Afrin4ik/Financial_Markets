from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional


@dataclass
class ChartRequest:
    ticker: str
    timeframe: str
    days_count: int
    from_: Optional[datetime] = None
    to_: Optional[datetime] = None

    def __post_init__(self) -> None:
        if not self.to_:
            self.to_ = datetime.now(timezone.utc)
        if not self.from_:
            self.from_ = self.to_ - timedelta(days=self.days_count)
