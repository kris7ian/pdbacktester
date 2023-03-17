import pandas as pd

from pdbacktester.function_registry import register
from pdbacktester.function_registry import register_and_inject


@register
def moving_average(column: pd.Series, window_length: int):
    column = column.rolling(window_length).mean()
    return column


@register
def highest(column: pd.Series, windows_length: int):
    # todo: remove implicit shift
    column = column.rolling(windows_length).max().shift()
    return column


@register
def lowest(column: pd.Series, windows_length: int):
    # todo: remove implicit shift
    column = column.rolling(windows_length).min().shift()
    return column


@register
def standard_dev(column: pd.Series, window_length: int):
    column = column.rolling(window_length).std()
    return column


@register
def cumulative_return(column: pd.Series, window_length: int):
    column = column.rolling(window_length).cumprod()
    return column


@register_and_inject("open", "close")
def atr(window_length: int, open: pd.Series, close: pd.Series):
    column = (open - close).rolling(window_length).mean()
    return column
