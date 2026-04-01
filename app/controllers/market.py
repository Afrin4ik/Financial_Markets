import logging

from fastapi import APIRouter, HTTPException, Query

from ..config.FIGI_map import FIGIs
from ..config.timeframe_map import TimeFrame
from ..models.schemas.market_request import ChartRequest
from ..models.schemas.market_response import ChartResponse
from ..services.market_service import build_chart_data


logger = logging.getLogger(__name__)


router = APIRouter(prefix="/market-data", tags=["market-data"])


@router.get("/chart")
def read_chart(
    ticker: str = Query(default=..., description="Название актива (ticker)"),
    timeframe: str = Query(default=..., description="Таймфрейм (timeframe)"),
    days_count: int = Query(default=..., ge=1, le=3650, description="Количество дней"),
) -> ChartResponse:
    try:
        ticker_key = ticker.strip().lower()
        timeframe_key = timeframe.strip()

        if ticker_key not in FIGIs:
            logger.warning(f"Неизвестный актив: {ticker_key}")
            raise HTTPException(
                status_code=422,
                detail={
                    "message": "Неизвестный актив",
                    "supported_assets": sorted(FIGIs.keys()),
                },
            )
        if timeframe_key not in TimeFrame:
            logger.warning(f"Неизвестный таймфрейм: {timeframe_key}")
            raise HTTPException(
                status_code=422,
                detail={
                    "message": "Неизвестный таймфрейм",
                    "supported_timeframes": sorted(TimeFrame.keys()),
                },
            )

        request = ChartRequest(
            ticker=ticker_key,
            days_count=days_count,
            timeframe=timeframe_key,
        )
        result = build_chart_data(request=request)
        return result
    except HTTPException:
        raise
    except RuntimeError as exc:
        logger.error(f"Ошибка при получении данных: {exc}")
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except ValueError as exc:
        logger.warning(f"Ошибка валидации: {exc}")
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("Непредвиденная ошибка в /market-data/chart")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера") from exc


@router.get("/assets")
def get_supported_assets() -> dict[str, list[str]]:
    return {"supported_assets": sorted(FIGIs.keys())}


@router.get("/timeframes")
def get_supported_timeframes() -> dict[str, list[str]]:
    return {"supported_timeframes": list(TimeFrame.keys())}
