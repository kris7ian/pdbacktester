from pdbacktester.classes import SeriesContainer


FUNCTION_REGISTRY = {}


def series_container(func):
    """
    The series_container makes sure that all the functions can
    handle arguments of type SeriesContainer by converting any
    arguments of that type to a pandas Series. It will also
    make sure that any value returned is of the type pd.Series.
    """

    def inner(*args, **kwargs):

        # the functions expect regular series, not containers
        # so we need to pass the series of the container instead
        # of the container itself, we don't have to worry because
        # we'll make sure the function returns a container again

        modified_args = []
        for arg in args:
            if isinstance(arg, SeriesContainer):
                modified_args.append(arg.series)
            else:
                modified_args.append(arg)

        modified_kwargs = {}
        for key, value in kwargs.items():
            if isinstance(value, SeriesContainer):
                modified_kwargs[key] = value.series
            else:
                modified_kwargs[key] = value

        return SeriesContainer(func(*modified_args, **modified_kwargs))

    FUNCTION_REGISTRY[func.__name__] = inner

    return inner


@series_container
def moving_average(column, window_length):
    column = column.rolling(window_length).mean()
    return column


@series_container
def highest(column, windows_length):
    column = column.rolling(windows_length).max().shift()
    return column


@series_container
def lowest(column, windows_length):
    column = column.rolling(windows_length).min().shift()
    return column


def weekday(df):
    return df["datetime"].dt.weekday + 1


def month(df):
    return df["datetime"].dt.month


def year(df):
    return df["datetime"].dt.year


def day(df):
    return df["datetime"].dt.day


def today(df):
    return df["datetime"]


def gap(df):
    return df["open"] / df["close"].shift(1) - 1
