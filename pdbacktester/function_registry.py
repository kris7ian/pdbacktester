from pdbacktester.series_container import SeriesContainer

FUNCTION_REGISTRY = {}
FUNCTION_REGISTRY_WITH_INJECTIONS = {}


def register_function(func, name):
    FUNCTION_REGISTRY[name or func.__name__] = func


def register_function_with_injections(func, name):
    FUNCTION_REGISTRY_WITH_INJECTIONS[name] = func


def register(func):
    """
    This decorator registers a function to the registry and
    makes sure that all the functions can handle arguments
    of type SeriesContainer by converting any arguments of
    that type to a pandas Series. It also makes sure that the
    returned Series is wrapped in a SeriesContainer.
    """

    def inner(*args, **kwargs):
        modified_args = transform_args(args)
        modified_kwargs = transform_kwargs(kwargs)
        return SeriesContainer(func(*modified_args, **modified_kwargs))

    register_function(inner, func.__name__)
    return inner


def register_and_inject(*columns):
    """
    This decorator does everything the register decorator
    does but also injects all passed *columns to be available
    for the function.
    """

    def wrapper(func):
        def inner(df, *args, **kwargs):
            modified_args = transform_args(args)
            modified_kwargs = transform_kwargs(kwargs)

            injected_args = []
            for col in columns:
                injected_args.append(df[col])

            return SeriesContainer(
                func(*modified_args, *injected_args, **modified_kwargs)
            )

        register_function_with_injections(inner, func.__name__)
        return inner

    return wrapper


def transform_args(args):
    modified_args = []
    for arg in args:
        if isinstance(arg, SeriesContainer):
            modified_args.append(arg.series)
        else:
            modified_args.append(arg)
    return modified_args


def transform_kwargs(kwargs):
    modified_kwargs = {}
    for key, value in kwargs.items():
        if isinstance(value, SeriesContainer):
            modified_kwargs[key] = value.series
        else:
            modified_kwargs[key] = value
    return modified_kwargs
