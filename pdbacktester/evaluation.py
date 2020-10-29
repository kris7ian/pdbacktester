import pandas as pd

from pdbacktester.classes import SeriesContainer
from pdbacktester import functions


def get_locals(df):
    locals_dict = dict(
        open=SeriesContainer(df["open"]),
        high=SeriesContainer(df["high"]),
        low=SeriesContainer(df["low"]),
        close=SeriesContainer(df["close"]),
        weekday=SeriesContainer(functions.weekday(df)),
        month=SeriesContainer(functions.month(df)),
        year=SeriesContainer(functions.year(df)),
        day=SeriesContainer(functions.day(df)),
    )

    functions_dict = functions.FUNCTION_REGISTRY

    return {**locals_dict, **functions_dict}


def evaluate_line(df, line):
    # todo: assert line has a condition
    locals_dict = get_locals(df)
    return eval(line, {'__builtins__': None}, locals_dict)


def get_signals(df, code_string):
    conditions = []
    lines = [s.strip() for s in code_string.strip().splitlines()]
    for i, line in enumerate(lines):
        try:
            condition = evaluate_line(df, line)
        except Exception as e:
            # Examples: SyntaxError
            print(f"There was an error on line: {line}")
            raise
        conditions.append(condition)

    conditions = pd.concat(conditions, axis=1)
    signals = conditions.all(axis=1)
    return signals
