import pandas as pd
import pytest

from pdbacktester.series_container import SeriesContainer
from pdbacktester.functions import FUNCTION_REGISTRY
from pdbacktester.functions import series_container


@pytest.fixture
def sample_series():
    yield pd.Series([1, 2, 3, 4, 5])


@pytest.fixture
def sample_decorated_function():
    @series_container
    def do_something(column):
        if not isinstance(column, pd.Series):
            raise ValueError("Expecting a series!")
        return column

    return do_something


def test_series_container_decorator(sample_decorated_function, sample_series):
    column = SeriesContainer(sample_series)
    column = sample_decorated_function(column)
    print(column)
    print(type(column))
    assert isinstance(column, SeriesContainer)


def test_function_registry(sample_decorated_function):
    assert "do_something" in FUNCTION_REGISTRY
