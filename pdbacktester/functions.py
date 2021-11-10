from pdbacktester.function_registry import register
from pdbacktester.function_registry import register_and_inject


@register
def moving_average(column, window_length):
    column = column.rolling(window_length).mean()
    return column


@register
def highest(column, windows_length):
    # todo: remove implicit shift
    column = column.rolling(windows_length).max().shift()
    return column


@register
def lowest(column, windows_length):
    # todo: remove implicit shift
    column = column.rolling(windows_length).min().shift()
    return column


@register
def standard_dev(column, window_length):
    column = column.rolling(window_length).std()
    return column


@register
def cumulative_return(column, window_length):
    column = column.rolling(window_length).cumprod()
    return column


@register_and_inject("open", "close")
def atr(window_length, open, close):
    column = (open - close).rolling(window_length).mean()
    return column
