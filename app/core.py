import os
import quandl

try:
    quandl.ApiConfig.api_key = os.environ["QUANDL_API_KEY"]
except:
    raise Exception("Need to set QUANDL_API_KEY envirnoment variable")


class Portfolio:
    """Portfolio of assets"""
    def __init__(self, assets):
        self.assets = assets

    def get_prices(self, start=None, end=None):
        """
        Download pricing data from quandl
        ----------
        Parameters
        ----------
        start - starting date
        end - ending date
        """
        data = quandl.get_table(
            'WIKI/PRICES',
            ticker=self.assets,
            qopts={'columns': ['date', 'ticker', 'adj_close']},
            date={
                'gte': start,
                'lte': end
            },
            paginate=True)
        data.set_index('date', inplace=True)
        data = data.pivot(columns='ticker')
        data.columns = [col[1] for col in data.columns]
        return data.dropna()

    def get_returns(self, start=None, end=None):
        prices = self.get_prices(start, end)
        return prices.pct_change().dropna()

    def get_cum_returns(self, start=None, end=None):
        returns = self.get_returns(start, end)
        returns = returns + 1
        return returns.cumprod() * 100


    def optimize(self):
        pass
