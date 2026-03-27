from tinkoff.invest import CandleInterval


TimeFrame: dict[str, CandleInterval] = {
    "5s": CandleInterval.CANDLE_INTERVAL_5_SEC,
    "1m": CandleInterval.CANDLE_INTERVAL_1_MIN,
    "2m": CandleInterval.CANDLE_INTERVAL_2_MIN,
    "3m": CandleInterval.CANDLE_INTERVAL_3_MIN,
    "5m": CandleInterval.CANDLE_INTERVAL_5_MIN,
    "15m": CandleInterval.CANDLE_INTERVAL_15_MIN,
    "30m": CandleInterval.CANDLE_INTERVAL_30_MIN,
    "1h": CandleInterval.CANDLE_INTERVAL_HOUR,
    "2h": CandleInterval.CANDLE_INTERVAL_2_HOUR,
    "4h": CandleInterval.CANDLE_INTERVAL_4_HOUR,
    "1d": CandleInterval.CANDLE_INTERVAL_DAY,
    "1w": CandleInterval.CANDLE_INTERVAL_WEEK,
    "1M": CandleInterval.CANDLE_INTERVAL_MONTH
}
