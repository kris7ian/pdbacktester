from pdbacktester.series_container import SeriesContainer


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

        return SeriesContainer(lambda: func(*modified_args, **modified_kwargs))

    FUNCTION_REGISTRY[func.__name__] = inner

    return inner


def series_container_inject(*columns):
    def wrapper(func):
        def inner(df, *args):
            modified_args = []
            for arg in args:
                if isinstance(arg, SeriesContainer):
                    modified_args.append(arg.series)
                else:
                    modified_args.append(arg)

            injected_args = []
            for col in columns:
                injected_args.append(df[col])

            return SeriesContainer(lambda: func(*modified_args, *injected_args))

        FUNCTION_REGISTRY[func.__name__] = inner
        return inner
    return wrapper


@series_container
def moving_average(column, window_length):
    column = column.rolling(window_length).mean()
    return column


@series_container
def highest(column, windows_length):
    # todo: remove implicit shift
    column = column.rolling(windows_length).max().shift()
    return column


@series_container
def lowest(column, windows_length):
    # todo: remove implicit shift
    column = column.rolling(windows_length).min().shift()
    return column


@series_container
def standard_dev(column, window_length):
    column = column.rolling(window_length).std()
    return column


@series_container
def cumulative_return(column, window_length):
    column = column.rolling(window_length).cumprod()
    return column


@series_container_inject("open", "close")
def atr(window_length, open, close):
    column = (open - close).rolling(window_length).mean()
    return column
