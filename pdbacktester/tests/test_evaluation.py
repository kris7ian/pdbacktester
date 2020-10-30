import pandas as pd
import pytest

from pdbacktester.evaluation import evaluate_line
from pdbacktester.evaluation import get_signals


@pytest.fixture()
def sample_data():
    df = pd.read_csv(
        "/Users/kristian/Development/python/pd-backtester/pdbacktester/tests/testing.csv",
    )
    df = df.tail(100)
    df["datetime"] = pd.to_datetime(df["datetime"])
    yield df


def test_sample_line_evaluations(sample_data):
    sample_line = "close > open"
    result = evaluate_line(sample_data, sample_line)
    assert isinstance(result, pd.Series)


def test_sample_line_evaluations_with_shift(sample_data):
    sample_line = "high > open[5]"
    result = evaluate_line(sample_data, sample_line)
    assert isinstance(result, pd.Series)


def test_sample_line_evaluations_equality_when_same_shift(sample_data):
    sample_line = "high[5] == high[5]"
    result = evaluate_line(sample_data, sample_line)
    assert isinstance(result, pd.Series)
    assert result.iloc[5:].all()


def test_sample_line_evaluations_with_mul(sample_data):
    sample_line = "high * 0 == 0"
    result = evaluate_line(sample_data, sample_line)
    assert isinstance(result, pd.Series)
    assert result.all()


def test_sample_evaluations_with_functions(sample_data):
    sample_line = "highest(high, 5) == 0"
    result = evaluate_line(sample_data, sample_line)
    assert isinstance(result, pd.Series)
    assert ~result.any()


def test_sample_evaluations_with_moving_average(sample_data):
    sample_line = "moving_average(high, 5) > close"
    result = evaluate_line(sample_data, sample_line)
    assert isinstance(result, pd.Series)
    assert result.any()


def test_evaluation_with_year(sample_data):
    sample_line = "year == 2019"
    result = evaluate_line(sample_data, sample_line)
    assert isinstance(result, pd.Series)
    assert result.all()


def test_evaluation_with_or(sample_data):
    sample_line = "(year == 2019) | (year == 0)"
    result = evaluate_line(sample_data, sample_line)
    assert isinstance(result, pd.Series)
    assert result.all()


def test_evaluation_with_and(sample_data):
    sample_line = "(year == 2019) & (year == 2019)"
    result = evaluate_line(sample_data, sample_line)
    assert isinstance(result, pd.Series)
    assert result.all()


def test_multiple_line_evaluation(sample_data):
    code_string = """
    open > close
    high * 0 == 0
    high / low > 1.0
    """
    signals = get_signals(sample_data, code_string)
    assert isinstance(signals, pd.Series)
