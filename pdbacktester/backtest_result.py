import pandas as pd


class BacktestResult:
    def __init__(self, signals: pd.Series, returns: pd.Series):
        self.signals = signals
        self.returns = returns

    @property
    def trades(self):
        pass
