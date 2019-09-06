import numpy as np
import os
import quandl

ROWS = 252 * 5 # number of prices rows to download

try:
    quandl.ApiConfig.api_key = os.environ["QUANDL_API_KEY"]
except:
    raise Exception("Need to set QUANDL_API_KEY envirnoment variable")


class Portfolio:
    """Portfolio of assets"""
    def __init__(self, assets=None):
        self.assets = assets or []

    def __setattr__(self, name, value):
        if name == 'assets': # reload prices every time assets are setted
            self.prices = self.load_prices(value, rows=ROWS)
        super().__setattr__(name, value)

    @staticmethod
    def load_prices(assets, **kwargs):
        """Download historical prices from Quandl"""
        if not assets:
            return None
        df = quandl.get(
            [f'WIKI/{asset}.11' for asset in assets],
            **kwargs
        )
        df.columns = assets
        return df.dropna()

    @property
    def returns(self):
        return self.prices.pct_change().dropna()

    @property
    def cum_returns(self):
        returns = self.returns + 1
        return returns.cumprod() * 100

    def random_weights(self):
        """Generate random weights for portfolio assets"""
        k = np.random.random(len(self.assets))
        return k / sum(k)

    def random_mu_sigma(self):
        """Calculate mu and sigma for portfolio with random weights"""
        returns = self.returns

        p = returns.mean().values
        w = self.random_weights()
        C = returns.cov().values

        mu = np.dot(w, p.T)
        sigma = np.sqrt(np.dot(np.dot(w, C), w.T))

        return mu, sigma

    def generate_random_portfolios(self, n):
        """Generates n random portfolio and returns array of mean returns and
        standard deviations"""
        return np.array([self.random_mu_sigma() for i in range(n)]).T

    def optimize(self):
        pass
