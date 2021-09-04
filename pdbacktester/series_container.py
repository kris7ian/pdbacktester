import pandas as pd


class SeriesContainer:
    """
    The SeriesContainer serves the only purpose of translating
    series_container_instance[n] to series_container_instance.shift(n)
    for simplicity for the enduser.
    """

    def __init__(self, series_or_func):
        if callable(series_or_func):
            self.series_func = series_or_func
            self.series_value = None
        elif isinstance(series_or_func, pd.Series):
            self.series_value = series_or_func
        else:
            raise ValueError(
                "SeriesContainer argument has to be a function or a Series"
            )

    @property
    def series(self):
        if self.series_value is None:
            self.series_value = self.series_func()
        return self.series_value

    def __add__(self, other):
        if isinstance(other, SeriesContainer):
            return self.series + other.series
        else:
            return self.series + other

    def __mul__(self, other):
        if isinstance(other, SeriesContainer):
            return self.series * other.series
        else:
            return self.series * other

    def __sub__(self, other):
        if isinstance(other, SeriesContainer):
            return self.series - other.series
        else:
            return self.series - other

    def __truediv__(self, other):
        if isinstance(other, SeriesContainer):
            return self.series / other.series
        else:
            return self.series / other

    def __lt__(self, other):
        if isinstance(other, SeriesContainer):
            return self.series < other.series
        else:
            return self.series < other

    def __le__(self, other):
        if isinstance(other, SeriesContainer):
            return self.series <= other.series
        else:
            return self.series <= other

    def __gt__(self, other):
        if isinstance(other, SeriesContainer):
            return self.series > other.series
        else:
            return self.series > other

    def __ge__(self, other):
        if isinstance(other, SeriesContainer):
            return self.series >= other.series
        else:
            return self.series >= other

    def __eq__(self, other):
        if isinstance(other, SeriesContainer):
            return self.series == other.series
        else:
            return self.series == other

    def __and__(self, other):
        if isinstance(other, SeriesContainer):
            return self.series & other.series
        else:
            return self.series & other

    def __or__(self, other):
        if isinstance(other, SeriesContainer):
            return self.series | other.series
        else:
            return self.series | other

    def __getitem__(self, i):
        if not isinstance(i, int):
            raise ValueError(f"'{i}' is not an integer!")
        if i < 0:
            raise IndexError("You are trying to peak into the future!")

        return self.series.shift(i)
