import numpy as np
import pandas as pd
import unittest
from unittest.mock import MagicMock

from app.portfolio import Portfolio

TICKERS = ['AMZN', 'FB', 'MSFT']
port = Portfolio()
port.load_prices = MagicMock(
    return_value=pd.DataFrame(
        np.random.randn(100, len(TICKERS)),
        range(100),
        TICKERS
    )
)


class TestPortfolio(unittest.TestCase):
    def test_blank(self):
        self.assertListEqual(port.assets, [])
        self.assertIsNone(port.prices, [])

    def test_setting(self):
        port.assets = TICKERS
        self.assertListEqual(port.assets, TICKERS)
        self.assertEqual(port.prices.shape[1], len(TICKERS))
        self.assertIsNotNone(port.prices)

    def test_random_weights(self):
        port.assets = TICKERS
        weights = port.random_weights()
        self.assertAlmostEqual(sum(weights), 1.0)

    def test_random_mu_sigma(self):
        port.assets = TICKERS
        mu, sigma = port.random_mu_sigma()
        self.assertIsNotNone(mu)
        self.assertIsNotNone(sigma)
        self.assertIsInstance(mu, float)
        self.assertIsInstance(sigma, float)

    def test_generate_random_portfolios(self):
        port.assets = TICKERS
        n = 50
        means, stds = port.generate_random_portfolios(n)
        self.assertEqual(means.shape, stds.shape, n)


if __name__ == '__main__':
    unittest.main()
