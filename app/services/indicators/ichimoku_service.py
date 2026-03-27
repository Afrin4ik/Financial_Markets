from dataclasses import dataclass
from typing import List
import numpy as np
from ...models.entities.candle import CandleData
from ...models.entities.ichimoku import IchimokuData


NUMPY_NAN = np.nan
T_s = 9
T_m = 26
T_l = 52


def calculate_line(candles: List[CandleData], time_frame: int) -> np.ndarray:
    if time_frame <= 0:
        raise ValueError("Timeframe must be greater than 0")

    count_candles: int = len(candles)

    highs = np.array([c.high for c in candles], dtype=np.float64)
    lows = np.array([c.low for c in candles], dtype=np.float64)

    result = np.full(count_candles, NUMPY_NAN, dtype=np.float64)
    for i in range(time_frame - 1, count_candles):
        start_ind = i - time_frame + 1
        end_ind = i + 1
        result[i] = (highs[start_ind:end_ind].max() + lows[start_ind:end_ind].min()) / 2.0

    return result


def shift_forward(values: np.ndarray, shift: int) -> np.ndarray:
    if shift <= 0:
        return values.copy()
    elif shift >= len(values):
        return np.full(len(values), NUMPY_NAN)

    result = np.empty(len(values))
    result[:shift] = NUMPY_NAN
    result[shift:] = values[:-shift]
    return result


def shift_backward(values: np.ndarray, shift: int) -> np.ndarray:
    if shift <= 0:
        return values.copy()
    elif shift >= len(values):
        return np.full(len(values), NUMPY_NAN)

    result = np.empty(len(values))
    result[:-shift] = values[shift:]
    result[-shift:] = NUMPY_NAN
    return result


def calculate_Ichimoku(candles: List[CandleData]) -> IchimokuData:
    Tenkan = calculate_line(candles, T_s)
    Kijun = calculate_line(candles, T_m)
    Senkou_A = shift_forward((Tenkan + Kijun) / 2.0, T_m)
    Senkou_B = shift_forward(calculate_line(candles, T_l), T_m)
    closes = np.array([c.close for c in candles])
    Chikou = shift_backward(closes, T_m)

    return IchimokuData(
        Tenkan=Tenkan,
        Kijun=Kijun,
        Senkou_A=Senkou_A,
        Senkou_B=Senkou_B,
        Chikou=Chikou
    )
