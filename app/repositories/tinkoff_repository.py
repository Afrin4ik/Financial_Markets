from ..config.settings import TOKEN
from tinkoff.invest import Client
# from datetime import datetime, timedelta, timezone
from ..models.entities.candle import CandleData
from ..config.FIGI_map import FIGIs
from ..config.timeframe_map import TimeFrame
from ..models.schemas.market_request import ChartRequest


def _quotation_to_float(money_value) -> float:
    return money_value.units + (money_value.nano / 1e9)


def get_candles_from_tinkoff(request: ChartRequest) -> list[CandleData]:
    if not TOKEN:
        raise RuntimeError("Токен API не найден!")

    with Client(TOKEN) as client:
        response = client.get_all_candles(
            instrument_id = FIGIs[request.figi],
            interval = TimeFrame[request.timeframe],
            from_=request.from_,
            to=request.to_
        )

        candles = []
        for candle in response:
            candles.append(CandleData(
                    open=_quotation_to_float(candle.open),
                    close=_quotation_to_float(candle.close),
                    low=_quotation_to_float(candle.low),
                    high=_quotation_to_float(candle.high),
                    volume=candle.volume,
                    time=candle.time
                ))
        # print(candles)
        return candles
