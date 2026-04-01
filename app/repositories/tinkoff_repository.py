import logging

from ..config.settings import TOKEN
from tinkoff.invest import Client
from ..models.entities.candle import CandleData
from ..config.FIGI_map import FIGIs
from ..config.timeframe_map import TimeFrame
from ..models.schemas.market_request import ChartRequest


logger = logging.getLogger(__name__)


def _quotation_to_float(value: object) -> float:
    units = getattr(value, "units", None)
    nano = getattr(value, "nano", None)
    if units is None or nano is None:
        raise ValueError("Некорректный формат денежного значения в ответе API")
    return float(units) + (float(nano) / 1e9)


def get_candles_from_tinkoff(request: ChartRequest) -> list[CandleData]:
    if not TOKEN:
        logger.critical("API токен не найден!")
        raise RuntimeError("API токен не найден!")

    figi = FIGIs.get(request.ticker)
    if not figi:
        logger.warning(f"FIGI не найден для актива: {request.ticker}")
        raise ValueError(f"Неизвестный актив: {request.ticker}")

    interval = TimeFrame.get(request.timeframe)
    if not interval:
        logger.warning(f"Интервал не найден для таймфрейма: {request.timeframe}")
        raise ValueError(f"Неизвестный таймфрейм: {request.timeframe}")

    try:
        with Client(TOKEN) as client:
            response = client.get_all_candles(
                instrument_id=figi,
                interval=interval,
                from_=request.from_,
                to=request.to_,
            )

            candles: list[CandleData] = []
            for candle in response:
                candles.append(
                    CandleData(
                        open=_quotation_to_float(candle.open),
                        close=_quotation_to_float(candle.close),
                        low=_quotation_to_float(candle.low),
                        high=_quotation_to_float(candle.high),
                        volume=float(candle.volume),
                        time=candle.time,
                    )
                )
            logger.info(f"Загружено {len(candles)} свечей из Tinkoff API для {request.ticker}/{request.timeframe}")
            return candles
    except ValueError:
        raise
    except Exception as exc:
        logger.exception(f"Ошибка при запросе свечей к Tinkoff API для {request.ticker}/{request.timeframe}")
        raise RuntimeError("Не удалось получить данные из внешнего API") from exc
