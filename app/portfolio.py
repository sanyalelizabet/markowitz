import os
import quandl

try:
    quandl.ApiConfig.api_key = os.environ["QUANDL_API_KEY"]
except:
    raise Exception("Need to set QUANDL_API_KEY envirnoment variable")


class Portfolio:
    """Portfolio of assets"""
    def __init__(self, assets=None):
        self.assets = assets or []

    def get_prices(self, start=None, end=None, rows=None):
        """
        Download historical adj.close data from quandl
        ----------
        Parameters
        ----------
        start - starting date
        end - ending date
        """
        if not self.assets:
            return None
        df = quandl.get(
            [f'WIKI/{asset}.11' for asset in self.assets],
            start_date=start,
            end_date=end,
            rows=rows
        )
        df.columns = self.assets
        return df.dropna()

    def get_returns(self, start=None, end=None):
        prices = self.get_prices(start, end)
        if prices is None:
            return None
        return prices.pct_change().dropna()

    def get_cum_returns(self, start=None, end=None):
        returns = self.get_returns(start, end)
        if returns is None:
            return None
        returns = returns + 1
        return returns.cumprod() * 100


    def optimize(self):
        pass
