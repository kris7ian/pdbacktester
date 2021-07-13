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
