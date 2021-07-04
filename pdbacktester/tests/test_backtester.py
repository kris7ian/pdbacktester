import pytest
import pandas as pd

from pdbacktester.backtester import Backtester
import pathlib


@pytest.fixture()
def sample_data():
    df = pd.read_csv(
        f"{pathlib.Path(__file__).parent.resolve()}/testing.csv"
    )
    df = df.tail(100)
    df["datetime"] = pd.to_datetime(df["datetime"])
    yield df


def test_backtester(sample_data):
    sample_code = """
    close > open
    """

    backtester = Backtester(sample_data, sample_code)
    backtester.run()
    assert backtester.signals is not None
