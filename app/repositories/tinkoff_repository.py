from ..config.settings import TOKEN
from tinkoff.invest import Client
from datetime import datetime, timedelta, timezone
from ..models.entities.candle import CandleData
from ..config.FIGI_map import FIGIs
from ..config.timeframe_map import TimeFrame

with Client(TOKEN) as client:
    response = client.get_all_candles(
        instrument_id = FIGIs["appl"],
        interval = TimeFrame["4h"],
        from_=datetime.now(timezone.utc) - timedelta(days=DAYS_NUMBER),
        to=datetime.now(timezone.utc)
    )

    candles = []
    for candle in response:
        candles.append(CandleData(
                open=(candle.open.units + (candle.open.nano / 1e9)),
                close=(candle.close.units + (candle.close.nano / 1e9)),
                low=(candle.low.units + (candle.low.nano) / 1e9),
                high=(candle.high.units + (candle.high.nano) / 1e9),
                volume=candle.volume,
                time=candle.time
            ))
    # print(candles)

