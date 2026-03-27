from dataclasses import dataclass


@dataclass
class CandleData:
    open: float
    close: float
    low: float
    high: float
    volume: float
    time: float
