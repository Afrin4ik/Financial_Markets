from ..repositories.tinkoff_repository import candles
import pandas as pd
import mplfinance as mpf
from ..models.entities.ichimoku import IchimokuData
from indicators.ichimoku_service import calculate_Ichimoku


# получаем данные о свечах, преобразуем их в DataFrame и устанавливаем индекс по времени
DF = pd.DataFrame(candles)
DF['time'] = pd.to_datetime(DF['time'])
DF.set_index('time', inplace=True)



# рассчитываем линии Ишимоку и создаем серии для каждой линии (используя индекс из DataFrame)
Ichimoku_data: IchimokuData = calculate_Ichimoku(candles)
Tenkan_series = pd.Series(Ichimoku_data.Tenkan, index=DF.index, dtype='float64')
Kijun_series = pd.Series(Ichimoku_data.Kijun, index=DF.index, dtype='float64')
Senkou_A_series = pd.Series(Ichimoku_data.Senkou_A, index=DF.index, dtype='float64')
Senkou_B_series = pd.Series(Ichimoku_data.Senkou_B, index=DF.index, dtype='float64')
Chikou_series = pd.Series(Ichimoku_data.Chikou, index=DF.index, dtype='float64')

additional_plot_dicts = []

if Tenkan_series.notna().any():
    additional_plot_dicts.append(mpf.make_addplot(Tenkan_series, color='red', width=1))
if Kijun_series.notna().any():
    additional_plot_dicts.append(mpf.make_addplot(Kijun_series, color='blue', width=1))
if Senkou_A_series.notna().any():
    additional_plot_dicts.append(mpf.make_addplot(Senkou_A_series, color='grey', width=1))
if Senkou_B_series.notna().any():
    additional_plot_dicts.append(mpf.make_addplot(Senkou_B_series, color='grey', width=1))
if Chikou_series.notna().any():
    additional_plot_dicts.append(mpf.make_addplot(Chikou_series, color='green', width=1))

mask_up = (Senkou_A_series > Senkou_B_series)
y1_up = Senkou_A_series.where(mask_up)
y2_up = Senkou_B_series.where(mask_up)

mask_down = (Senkou_A_series < Senkou_B_series)
y1_down = Senkou_A_series.where(mask_down)
y2_down = Senkou_B_series.where(mask_down)

filling_dicts = []

if y1_up.notna().any() and y2_up.notna().any():
    filling_dicts.append(
        {
            'y1': y1_up.values.tolist(),
            'y2': y2_up.values.tolist(),
            'color': '#9be69b',
            'alpha': 0.25
        }
    )

if y1_down.notna().any() and y2_down.notna().any():
    filling_dicts.append(
    {
            'y1': y1_down.values.tolist(),
            'y2': y2_down.values.tolist(),
            'color': '#f2a2a2',
            'alpha': 0.25
        }
    )



# настраиваем параметры графика для mplfinance
plot_kwargs = {
    'data': DF,
    'title': 'Asset Chart',
    'type': 'candle',
    'style': 'yahoo', # charles, yahoo
    'volume': True,
    # 'tight_layout': True # автоматически заполняет шрафик на всё окно (не всегда работает качественно)
    'scale_padding': {'left': 0, 'right': 0.75, 'top': 0.3, 'bottom': 0.55},
    # 'figratio': (16,9),
    'figscale': 1.3
    # 'style': 'nightclouds'
    # 'returnfig': True
}

if additional_plot_dicts:
    plot_kwargs['addplot'] = additional_plot_dicts

if filling_dicts:
    plot_kwargs['fill_between'] = filling_dicts
