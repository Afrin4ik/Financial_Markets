from dataclasses import dataclass
from datetime import datetime


@dataclass
class CandleData:
    open: float
    close: float
    low: float
    high: float
    volume: float
    time: datetime
