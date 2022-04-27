import pandas as pd
import pytest

from pdbacktester.function_registry import FUNCTION_REGISTRY
from pdbacktester.function_registry import FUNCTION_REGISTRY_WITH_INJECTIONS
from pdbacktester.function_registry import get_functions_with_injections
from pdbacktester.function_registry import register
from pdbacktester.function_registry import register_and_inject
from pdbacktester.function_registry import register_function
from pdbacktester.function_registry import register_function_with_injections
from pdbacktester.series_container import SeriesContainer


def my_func():
    pass


@pytest.fixture()
def series_container():
    return SeriesContainer(pd.Series([1, 2, 3]))


def test_register_function():
    register_function(my_func, "my_func")
    assert "my_func" in FUNCTION_REGISTRY


def test_register_function_with_injections():
    register_function_with_injections(my_func, "my_func")
    assert "my_func" in FUNCTION_REGISTRY_WITH_INJECTIONS


def test_register_decorator(series_container):
    @register
    def my_func(sc, sc2):
        return sc, sc2

    assert "my_func" in FUNCTION_REGISTRY


def test_register_decorator_transforms_args_kwargs(series_container):
    @register
    def my_func(sc):
        return sc

    sc = my_func(series_container)
    assert isinstance(sc, SeriesContainer)
    sc = my_func(sc=series_container)
    assert isinstance(sc, SeriesContainer)


def test_functions_in_inject_registry_are_not_cached():
    data = {"open": [1, 1, 1], "close": [2, 2, 2]}
    df = pd.DataFrame(data)

    @register_and_inject("open", "close")
    def my_func(multiplier, open, close):
        return multiplier * (open + close)

    result = my_func(df, 2)
    assert result.series_func is None
    assert result.series_value is not None


def test_functions_in_registry_are_not_cached(series_container):
    @register
    def my_func(sc):
        return sc

    result = my_func(series_container)
    assert result.series_func is None
    assert result.series_value is not None


def test_register_and_inject():
    data = {"open": [1, 1, 1], "close": [2, 2, 2]}
    df = pd.DataFrame(data)

    @register_and_inject("open", "close")
    def my_func(open, close):
        return open + close

    assert "my_func" in FUNCTION_REGISTRY_WITH_INJECTIONS

    result = my_func(df)
    assert result.series.tolist() == [3, 3, 3]


def test_register_and_inject_with_extra_arg():
    data = {"open": [1, 1, 1], "close": [2, 2, 2]}
    df = pd.DataFrame(data)

    @register_and_inject("open", "close")
    def my_func(multiplier, open, close):
        return multiplier * (open + close)

    assert "my_func" in FUNCTION_REGISTRY_WITH_INJECTIONS

    result = my_func(df, 2)
    assert result.series.tolist() == [6, 6, 6]


def test_get_functions_adds_df_as_first_argument():
    data = {"open": [1, 1, 1], "close": [2, 2, 2]}
    df = pd.DataFrame(data)

    @register_and_inject("open", "close")
    def my_func(multiplier, open, close):
        return multiplier * (open + close)

    functions = get_functions_with_injections(df)
    result = functions["my_func"](2)
    assert result.series.tolist() == [6, 6, 6]