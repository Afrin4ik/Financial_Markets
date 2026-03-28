from fastapi import APIRouter, HTTPException, Query

from ..config.FIGI_map import FIGIs
from ..config.timeframe_map import TimeFrame
from ..models.schemas.market_request import ChartRequest
from ..models.schemas.market_response import ChartResponse
from ..services.market_service import build_chart_data


router = APIRouter(prefix="/market", tags=["market"])


@router.get("/chart")
def read_chart(
    ticker: str = Query(default=..., description="Название актива (ticker)"),
    timeframe: str = Query(default=..., description="Таймфрейм (timeframe)"),
    days_count: int = Query(default=..., ge=1, le=3650, description="Количество дней"),
) -> ChartResponse:
    ticker_key = ticker.strip().lower()
    timeframe_key = timeframe.strip()

    if ticker_key not in FIGIs:
        raise HTTPException(
            status_code=422,
            detail={
                "message": "Неизвестный актив",
                "supported_assets": sorted(FIGIs.keys())
            },
        )
    if timeframe_key not in TimeFrame:
        raise HTTPException(
            status_code=422,
            detail={
                "message": "Неизвестный таймфрейм",
                "supported_timeframes": sorted(TimeFrame.keys()),
            },
        )

    request = ChartRequest(ticker=ticker_key, days_count=days_count, timeframe=timeframe_key)

    try:
        return build_chart_data(request=request)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/assets")
def get_supported_assets() -> dict[str, list[str]]:
    return {"supported_assets": sorted(FIGIs.keys())}


@router.get("/timeframes")
def get_supported_timeframes() -> dict[str, list[str]]:
    return {"supported_timeframes": TimeFrame.keys()}
