import pandas as pd

import pdbacktester.constants
from pdbacktester import functions
from pdbacktester.series_container import SeriesContainer
from pdbacktester.errors import EvaluationError


def get_variables(df: pd.DataFrame) -> dict:
    return dict(
        open=SeriesContainer(df["open"]),
        high=SeriesContainer(df["high"]),
        low=SeriesContainer(df["low"]),
        close=SeriesContainer(df["close"]),
        weekday=SeriesContainer(lambda: pdbacktester.constants.weekday(df)),
        month=SeriesContainer(lambda: pdbacktester.constants.month(df)),
        year=SeriesContainer(lambda: pdbacktester.constants.year(df)),
        day=SeriesContainer(lambda: pdbacktester.constants.day(df)),
        today=SeriesContainer(lambda: pdbacktester.constants.today(df)),
        gap=SeriesContainer(lambda: pdbacktester.constants.gap(df)),
    )


def get_locals(df: pd.DataFrame):
    """
    Collects all variables that should be available at runtime
    for the `eval` call in `evaluate_line`.
    """
    variables = get_variables(df)
    functions_dict = functions.FUNCTION_REGISTRY

    return {**variables, **functions_dict}


def assert_has_comparator(line: str):
    comparators = [">", "<", ">=", "<=", "=="]
    has_comparator = any([cmp in line for cmp in comparators])
    if not has_comparator:
        raise SyntaxError("Condition needs a comparator.")


def evaluate_line(df: pd.DataFrame, line: str):
    assert_has_comparator(line)
    locals_dict = get_locals(df)
    return eval(line, {"__builtins__": None}, locals_dict)


def get_signals(df: pd.DataFrame, code_string: str):
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
