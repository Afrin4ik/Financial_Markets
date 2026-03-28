import numpy as np

from ...models.schemas.market_response import CloudBandResponse


def _to_optional_float_list(values: np.ndarray) -> list[float | None]:
    return [None if np.isnan(v) else float(v) for v in values]


def build_cloud_bands(senkou_a: np.ndarray, senkou_b: np.ndarray) -> list[CloudBandResponse]:
    mask_up = senkou_a > senkou_b
    mask_down = senkou_a < senkou_b

    up_y1 = np.where(mask_up, senkou_a, np.nan)
    up_y2 = np.where(mask_up, senkou_b, np.nan)
    down_y1 = np.where(mask_down, senkou_a, np.nan)
    down_y2 = np.where(mask_down, senkou_b, np.nan)

    result: list[CloudBandResponse] = []

    if not np.isnan(up_y1).all() and not np.isnan(up_y2).all():
        result.append(
            CloudBandResponse(
                trend="up",
                y1=_to_optional_float_list(up_y1),
                y2=_to_optional_float_list(up_y2),
                color="#9be69b",
                alpha=0.25,
            )
        )

    if not np.isnan(down_y1).all() and not np.isnan(down_y2).all():
        result.append(
            CloudBandResponse(
                trend="down",
                y1=_to_optional_float_list(down_y1),
                y2=_to_optional_float_list(down_y2),
                color="#f2a2a2",
                alpha=0.25,
            )
        )

    return result
