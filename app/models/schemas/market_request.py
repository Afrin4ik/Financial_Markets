import logging
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional


logger = logging.getLogger(__name__)


@dataclass
class ChartRequest:
    ticker: str
    timeframe: str
    days_count: int
    from_: Optional[datetime] = None
    to_: Optional[datetime] = None

    def __post_init__(self) -> None:
        self.ticker = self.ticker.strip().lower()
        self.timeframe = self.timeframe.strip()

        if not self.ticker:
            logger.warning("Ошибка валидации: ticker не может быть пустым")
            raise ValueError("ticker не может быть пустым")
        if not self.timeframe:
            logger.warning("Ошибка валидации: timeframe не может быть пустым")
            raise ValueError("timeframe не может быть пустым")
        if self.days_count <= 0:
            logger.warning(f"Ошибка валидации: days_count={self.days_count} (должен быть > 0)")
            raise ValueError("days_count должен быть больше 0")

        if not self.to_:
            self.to_ = datetime.now(timezone.utc)
        elif self.to_.tzinfo is None:
            self.to_ = self.to_.replace(tzinfo=timezone.utc)

        if not self.from_:
            self.from_ = self.to_ - timedelta(days=self.days_count)
        elif self.from_.tzinfo is None:
            self.from_ = self.from_.replace(tzinfo=timezone.utc)

        if self.from_ >= self.to_:
            logger.warning(f"Ошибка валидации: период некорректен {self.from_} >= {self.to_}")
            raise ValueError("Период некорректен: from_ должен быть меньше to_")
