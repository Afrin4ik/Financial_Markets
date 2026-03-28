from datetime import datetime
from pydantic import BaseModel, Field


class CandleResponse(BaseModel):
    open: float
    close: float
    low: float
    high: float
    volume: float
    time: datetime


class IchimokuResponse(BaseModel):
    tenkan: list[float | None]
    kijun: list[float | None]
    senkou_a: list[float | None]
    senkou_b: list[float | None]
    chikou: list[float | None]


class CloudBandResponse(BaseModel):
    trend: str = Field(description="up или down")
    y1: list[float | None]
    y2: list[float | None]
    color: str
    alpha: float


class ChartResponse(BaseModel):
    ticker: str
    timeframe: str
    days_count: int
    candles: list[CandleResponse]
    ichimoku: IchimokuResponse
    cloud: list[CloudBandResponse]
