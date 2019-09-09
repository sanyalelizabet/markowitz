import numpy as np
import pandas as pd
import os
import quandl

from .dataframe import Data


class Portfolio:
    """Portfolio of assets"""
    def __init__(self, assets=None, weights=None):
        self.assets = assets or []
        self.weights = weights

    def set_random_weights(self, n):
        """Generate random weights for portfolio assets"""
        k = np.random.random(len(self.assets))
        self.weights =  k / sum(k)

    def calculate_mean(self, returns):
        """Calculates expected return (ann.) of current portfolio"""
        returns = returns.mean().values
        return (1. + np.dot(self.weights, returns.T))**252 - 1.

    def calculate_std(self, returns):
        """Calculates standard deviation (ann.) of current portfolio"""
        C = returns.cov().values
        return np.sqrt(np.dot(np.dot(self.weights, C), self.weights.T) * 252)

    def calculate_ratios(self, returns):
        """Calculate exp_return, std, sharpe_ratio"""
        self.mu = self.calculate_mean(returns)
        self.std = self.calculate_std(returns)
        self.sharpe = self.mu / self.std

    @classmethod
    def random_portfolios(cls, assets, n, returns=None):
        """Generates n random portfolio and returns array of mean returns and
        standard deviations"""
        i = 0
        while i < n:
            portfolio = cls(assets=assets)
            portfolio.set_random_weights()
            if returns:
                portfolio.calculate_ratios()
            yield portfolio
            i += 1
