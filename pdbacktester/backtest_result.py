class BacktestResult:
    def __init__(self, signals, returns):
        self.signals = signals
        self.returns = returns

    @property
    def trades(self):
        pass
