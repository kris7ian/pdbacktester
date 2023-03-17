import pandas as pd

from pdbacktester.constants import Columns


def weekday(df: pd.DataFrame):
    return df["datetime"].dt.weekday + 1


def month(df: pd.DataFrame):
    return df["datetime"].dt.month


def year(df: pd.DataFrame):
    return df["datetime"].dt.year


def day(df: pd.DataFrame):
    return df["datetime"].dt.day


def today(df: pd.DataFrame):
    return df["datetime"]


def gap(df: pd.DataFrame):
    return df[Columns.OPEN] / df[Columns.CLOSE].shift(1) - 1
