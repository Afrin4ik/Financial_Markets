from dataclasses import dataclass
import numpy as np


@dataclass
class IchimokuData:
    Tenkan: np.ndarray
    Kijun: np.ndarray
    Senkou_A: np.ndarray
    Senkou_B: np.ndarray
    Chikou: np.ndarray
