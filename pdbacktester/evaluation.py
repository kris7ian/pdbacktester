import pandas as pd

from pdbacktester import functions
from pdbacktester.classes import SeriesContainer
from pdbacktester.errors import EvaluationError


def get_locals(df):
    locals_dict = dict(
        open=SeriesContainer(df["open"]),
        high=SeriesContainer(df["high"]),
        low=SeriesContainer(df["low"]),
        close=SeriesContainer(df["close"]),
        weekday=SeriesContainer(lambda: functions.weekday(df)),
        month=SeriesContainer(lambda: functions.month(df)),
        year=SeriesContainer(lambda: functions.year(df)),
        day=SeriesContainer(lambda: functions.day(df)),
        today=SeriesContainer(lambda: functions.today(df)),
        gap=SeriesContainer(lambda: functions.gap(df)),
    )

    functions_dict = functions.FUNCTION_REGISTRY

    return {**locals_dict, **functions_dict}


def check_for_comparator(line):
    comparators = [">", "<", ">=", "<=", "=="]
    has_comparator = any([cmp in line for cmp in comparators])
    if not has_comparator:
        raise SyntaxError("Condition needs a comparator.")


def evaluate_line(df, line):
    check_for_comparator(line)
    locals_dict = get_locals(df)
    return eval(line, {"__builtins__": None}, locals_dict)


def get_signals(df, code_string):
    conditions = []
    lines = [s.strip() for s in code_string.strip().splitlines()]
    for i, line in enumerate(lines):
        try:
            condition = evaluate_line(df, line)
        except Exception as e:
            # Examples: SyntaxError
            raise EvaluationError(f"There was an error on line {i}: {line}")
        conditions.append(condition)

    conditions = pd.concat(conditions, axis=1)
    signals = conditions.all(axis=1)
    return signals
