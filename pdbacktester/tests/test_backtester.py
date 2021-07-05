import pathlib

import numpy as np
import pandas as pd
import pytest

from pdbacktester.backtester import Backtester


@pytest.fixture()
def sample_data_large():
    df = pd.read_csv(f"{pathlib.Path(__file__).parent.resolve()}/testing.csv")
    df = df.tail(100)
    df["datetime"] = pd.to_datetime(df["datetime"])
    yield df


@pytest.fixture()
def sample_data_small():
    data = [
        dict(open=1, high=1.1, low=0.9, close=1.05),
        dict(open=1.02, high=1.06, low=0.98, close=1.04),
        dict(open=1.04, high=1.2, low=1.02, close=1.15),
        dict(open=1.14, high=1.24, low=1.1, close=1.1),
        dict(open=1.12, high=1.24, low=1.1, close=2.2),
        dict(open=1.12, high=1.24, low=1.1, close=1.1),
    ]
    return pd.DataFrame(data)


@pytest.fixture()
def sample_code():
    return """
    close > open
    """


def test_backtester(sample_data_large, sample_code):
    backtester = Backtester(sample_data_large, sample_code)
    backtester.run(holding_period=3)
    assert backtester.signals is not None


def test_calculate_return(sample_data_small, sample_code):
    backtester = Backtester(sample_data_small, sample_code)
    returns = backtester.calculate_market_return()
    expected_returns = pd.Series(
        [
            np.nan,
            -0.00952380952380949,
            0.10576923076923062,
            -0.04347826086956508,
            1,
            -0.5,
        ]
    )
    pd.testing.assert_series_equal(returns, expected_returns, check_names=False)


def test_get_signals(sample_data_small, sample_code):
    backtester = Backtester(sample_data_small, sample_code)
    signals = backtester.get_signals()
    expected_signals = pd.Series([1, 1, 1, np.nan, 1, np.nan])
    pd.testing.assert_series_equal(signals, expected_signals, check_names=False)


def test_calculate_strategy_returns_single_period(sample_data_small, sample_code):
    backtester = Backtester(sample_data_small, sample_code)
    signals = backtester.get_signals()

    market_returns = backtester.calculate_market_return()
    strategy_returns = backtester.calculate_strategy_return(holding_period=1)

    # one period returns are next days return
    expected_returns = market_returns.shift(-1) * signals
    expected_returns = expected_returns.fillna(0)

    pd.testing.assert_series_equal(strategy_returns, expected_returns)


@pytest.mark.xfail
def test_calculate_strategy_returns_multiple_periods(sample_data_small, sample_code):
    backtester = Backtester(sample_data_small, sample_code)
    signals = backtester.get_signals()

    market_returns = backtester.calculate_market_return()
    strategy_returns = backtester.calculate_strategy_return(holding_period=2)

    # one period returns are next days return
    expected_returns = market_returns.shift(-1) * signals
    expected_returns = expected_returns.fillna(0)

    pd.testing.assert_series_equal(strategy_returns, expected_returns)
