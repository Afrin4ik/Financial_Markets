import numpy as np

from ..models.schemas.market_request import ChartRequest
from ..models.schemas.market_response import CandleResponse, ChartResponse, IchimokuResponse

from ..repositories.tinkoff_repository import get_candles_from_tinkoff
from .indicators.ichimoku_service import calculate_Ichimoku
from .indicators.cloudband_service import build_cloud_bands


def _to_optional_float_list(values: np.ndarray) -> list[float | None]:
    return [None if np.isnan(v) else float(v) for v in values]


def build_chart_data(request: ChartRequest) -> ChartResponse:
    candles = get_candles_from_tinkoff(request)
    if not candles:
        raise ValueError("По выбранным параметрам свечей не найдено")

    ichimoku = calculate_Ichimoku(candles)

    cloud = build_cloud_bands(ichimoku.Senkou_A, ichimoku.Senkou_B)

    return ChartResponse(
        ticker=request.ticker,
        timeframe=request.timeframe,
        days_count=request.days_count,
        candles=[
            CandleResponse(
                open=c.open,
                close=c.close,
                low=c.low,
                high=c.high,
                volume=float(c.volume),
                time=c.time,
            )
            for c in candles
        ],
        ichimoku=IchimokuResponse(
            tenkan=_to_optional_float_list(ichimoku.Tenkan),
            kijun=_to_optional_float_list(ichimoku.Kijun),
            senkou_a=_to_optional_float_list(ichimoku.Senkou_A),
            senkou_b=_to_optional_float_list(ichimoku.Senkou_B),
            chikou=_to_optional_float_list(ichimoku.Chikou),
        ),
        cloud=cloud,
    )
