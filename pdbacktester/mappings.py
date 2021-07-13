import pdbacktester.constants
from pdbacktester import functions

function_map = {
    "average": functions.moving_average,
    "highest": functions.highest,
    "lowest": functions.lowest,
}

keyword_map = {
    "open": "open",
    "high": "high",
    "low": "low",
    "close": "close",
    "change": "pct_change",
    "high_pct": "high_pct",
    "low_pct": "low_pct",
    "gap_pct": "gap_pct",
    "weekday": pdbacktester.constants.weekday,
    "month": pdbacktester.constants.month,
}


def register_function(name, function):
    function_map[name] = function


def register_variable(name, column_or_function):
    keyword_map[name] = column_or_function
