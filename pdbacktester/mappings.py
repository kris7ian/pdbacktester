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
    "weekday": functions.weekday,
    "month": functions.month,
}
