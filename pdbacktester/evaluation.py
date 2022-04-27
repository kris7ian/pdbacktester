import pandas as pd

import pdbacktester.constants
import pdbacktester.variables
from pdbacktester.constants import Columns
from pdbacktester.errors import EvaluationError
from pdbacktester.function_registry import get_functions_with_injections
from pdbacktester.function_registry import get_regular_functions
from pdbacktester.series_container import SeriesContainer


def get_variables(df: pd.DataFrame) -> dict:
    return dict(
        open=SeriesContainer(df[Columns.OPEN]),
        high=SeriesContainer(df[Columns.HIGH]),
        low=SeriesContainer(df[Columns.LOW]),
        close=SeriesContainer(df[Columns.CLOSE]),
        weekday=SeriesContainer(lambda: pdbacktester.variables.weekday(df)),
        month=SeriesContainer(lambda: pdbacktester.variables.month(df)),
        year=SeriesContainer(lambda: pdbacktester.variables.year(df)),
        day=SeriesContainer(lambda: pdbacktester.variables.day(df)),
        today=SeriesContainer(lambda: pdbacktester.variables.today(df)),
        gap=SeriesContainer(lambda: pdbacktester.variables.gap(df)),
    )


def get_functions(df: pd.DataFrame) -> dict:
    regular_functions = get_regular_functions()
    functions_with_injections = get_functions_with_injections(df)
    return {**regular_functions, **functions_with_injections}


def get_locals(df: pd.DataFrame):
    """
    Collects all variables that should be available at runtime
    for the `eval` call in `evaluate_line`.
    """
    variables = get_variables(df)
    functions_dict = get_functions(df)

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
