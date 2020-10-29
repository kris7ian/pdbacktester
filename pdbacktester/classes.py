class SeriesContainer:
    """
    The SeriesContainer serves the only purpose of translating
    series_container_instance[n] to series_container_instance.shift(n)
    for simplicity for the enduser.
    """

    def __init__(self, series):
        self.series = series

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

    def __getitem__(self, i):
        if not isinstance(i, int):
            raise ValueError(f"'{i}' is not an integer!")
        if i < 0:
            raise IndexError("You are trying to peak into the future!")

        return self.series.shift(i)
