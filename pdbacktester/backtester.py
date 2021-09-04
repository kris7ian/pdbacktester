import numpy as np
import pandas as pd

from pdbacktester.backtest_result import BacktestResult
from pdbacktester.errors import EvaluationError
from pdbacktester.evaluation import assert_has_comparator
from pdbacktester.evaluation import get_locals


class Backtester:
    def __init__(self, df, code):
        assert isinstance(df, pd.DataFrame), "df has to be a pandas DataFrame."
        assert isinstance(code, str), "code has to be a string."

        self.df = df.copy()
        self.code = code
        self.conditions = None
        self.signals = None
        self.market_returns = None
        self.strategy_returns = None
        self.result = None

    def run(self, holding_period):
        self.signals = self.get_signals()
        self.market_returns = self.calculate_market_return()
        self.strategy_returns = self.calculate_strategy_return(holding_period)
        self.result = BacktestResult(self.signals, self.market_returns)
        return self.result

    def convert_code_to_conditions(self):
        conditions = []
        lines = [s.strip() for s in self.code.strip().splitlines()]
        for i, line in enumerate(lines):
            try:
                condition = self.evaluate_code_line(line)
            except Exception as e:
                # Examples: SyntaxError
                raise EvaluationError(f"There was an error on line {i}: {line}")
            conditions.append(condition)
        return pd.concat(conditions, axis=1)

    def get_signals(self):
        self.conditions = self.convert_code_to_conditions()
        signals = self.conditions.all(axis=1)
        signals[~signals] = np.nan
        self.signals = signals
        return signals

    def get_random_signals(self, n):
        pass

    def evaluate_code_line(self, line):
        assert_has_comparator(line)
        locals_dict = get_locals(self.df)
        return eval(line, {"__builtins__": None}, locals_dict)

    def calculate_market_return(self):
        previous_close = self.df["close"].shift(1)
        self.market_returns = (self.df["close"] / previous_close) - 1
        return self.market_returns

    def calculate_strategy_return(self, holding_period):
        if holding_period == 1:
            # don't forward fill signals
            positions = self.signals
        else:
            positions = self.signals.fillna(method="ffill", limit=holding_period)
        returns = self.market_returns.shift(-1) * positions
        return returns.fillna(0)
