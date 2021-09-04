pdbacktester
==============

![example workflow](https://github.com/kris7ian/pdbacktester/actions/workflows/python-app.yml/badge.svg)


Installation
------------

    $ pip install pdbacktester


Quick Usage
-----
```python
import pandas as pd
from pdbacktester import Backtester

# Read data, assumes "open", "high", "low", "close" columns
# are present in the dataframe
df = pd.read_csv("/path/to/your/data.csv")

# Set up conditions
code = """
close < moving_average(close, 8)
close > open
"""

# Run backtest
backtester = Backtester(df, code)
results = backtester.run()
```

