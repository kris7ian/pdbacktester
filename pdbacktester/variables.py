from pdbacktester.constants import Columns


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
    return df[Columns.OPEN] / df[Columns.CLOSE].shift(1) - 1
