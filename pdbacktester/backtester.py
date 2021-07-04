import pandas as pd

from pdbacktester.backtest_result import BacktestResult
from pdbacktester.errors import EvaluationError
from pdbacktester.evaluation import check_for_comparator, get_locals


class Backtester:
    def __init__(self, df, code):
        assert isinstance(df, pd.DataFrame), "df has to be a pandas DataFrame."
        assert isinstance(code, str), "code has to be a string."

        self.df = df.copy()
        self.code = code
        self.signals = None
        self.market_returns = None
        self.strategy_returns = None
        self.result = None

    def run(self, holding_period):
        self.signals = self.get_signals()
        self.market_returns = self.calculate_market_return()
        self.strategy_returns = self.calculate_strategy_return(holding_period)
        self.result = BacktestResult(self.signals, self.returns)
        return self.result

    def get_signals(self):
        conditions = []
        lines = [s.strip() for s in self.code.strip().splitlines()]
        for i, line in enumerate(lines):
            try:
                condition = self.evaluate_code_line(line)
            except Exception as e:
                # Examples: SyntaxError
                raise EvaluationError(f"There was an error on line {i}: {line}")
            conditions.append(condition)

        conditions = pd.concat(conditions, axis=1)
        signals = conditions.all(axis=1)
        return signals

    def get_random_signals(self, n):
        pass

    def evaluate_code_line(self, line):
        check_for_comparator(line)
        locals_dict = get_locals(self.df)
        return eval(line, {"__builtins__": None}, locals_dict)

    def calculate_return(self):
        previous_close = self.df["close"].shift(-1)
        return previous_close / self.df["close"]
