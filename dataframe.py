import os
import quandl

ROWS = 252 * 5  # number of prices rows to download

try:
    quandl.ApiConfig.api_key = os.environ["QUANDL_API_KEY"]
except KeyError:
    raise Exception("Need to set QUANDL_API_KEY envirnoment variable")


class StockDataFrame:
    def __init__(self, assets):
        self.assets = assets
        self._adj_close = None

    def download(self, **kwargs):
        """Download historical prices from Quandl"""
        if not self.assets:
            return None
        df = quandl.get(
            [f'WIKI/{asset}.11' for asset in self.assets],  # 11 - adj_close
            **kwargs
        )
        df.columns = self.assets
        self._adj_close = df.dropna()

    @property
    def adj_close(self):
        return self._adj_close or self.download()

    @property
    def returns(self):
        return self.prices.pct_change().dropna()

    @property
    def cum_returns(self):
        returns = self.returns + 1
        return returns.cumprod() * 100
