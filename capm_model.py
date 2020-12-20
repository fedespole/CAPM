import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as sci
import pandas_datareader as pd
from datetime import date


class Portfolio:

    def __init__(self, num_assets, lab):
        self.A = num_assets
        self.N = 35000                                  # Number of simulated portfolios
        self.TradingDays = 253                          # NYSE and NASDAQ had 253 trading days a year in 2020
        self.labels = lab                               # Ticker list of the chosen assets
        self.portfolios = np.zeros((3, self.N))         # Each portfolio has 3 values (Volatility, Yield, Sharpe Ratio)
        self.rates = []                                 # List used to save weights to build optimal/safest portfolios
        self.frontierY = np.linspace(0, 50, 200)        # Initializing frontier bounds, value will be updated afterwards
        self.frontierX = []
        self.RiskFreeRate = pd.DataReader("DGS3MO", "fred").iat[-1, 0]  # Updated 3 Month US Treasury Bill Rate

    def build_simulation(self):

        asset_average, cov_table = self.download_yahoo_data()
        np.random.seed(35)

        for i in range(self.N):
            weights = np.random.random(self.A)          # Random weights to simulate different portfolios
            weights /= np.sum(weights)
            self.rates.append(weights)
            results = self.portfolio_variables(weights, asset_average, cov_table)

            self.portfolios[0, i] = results[1]                                          # Volatility
            self.portfolios[1, i] = results[0]                                          # Yield
            self.portfolios[2, i] = (results[0] - self.RiskFreeRate) / results[1]       # Sharpe Ratio

        min_vol_index, max_yield_index = np.argmin(self.portfolios[0]), np.argmax(self.portfolios[1])
        min_x, min_y = self.portfolios[0, min_vol_index], self.portfolios[1, min_vol_index]         # Min volatility
        max_x, max_y = self.portfolios[0, max_yield_index], self.portfolios[1, max_yield_index]     # Max yield
        self.frontierY = np.linspace(min_y, max_y, 200)  # Bounds for efficient frontier

        sharpe_index = np.argmax(self.portfolios[2])
        sh_x, sh_y = self.portfolios[0, sharpe_index], self.portfolios[1, sharpe_index]         # Maximum Sharpe Ratio

        safest_portfolio = self.rates[min_vol_index]          # Portfolio with minimum volatility
        safest_portfolio = [round(x * 100, 3) for x in safest_portfolio]

        optimal_portfolio = self.rates[sharpe_index]          # Most performant portfolio according to Sharpe's theory
        optimal_portfolio = [round(x * 100, 3) for x in optimal_portfolio]

        self.efficient_frontier(asset_average, cov_table)
        self.display_simulation(sh_x, sh_y, min_x, min_y)
        self.portfolios_allocation(optimal_portfolio, safest_portfolio, sh_x, sh_y, min_x, min_y)

    def download_yahoo_data(self):

        today = date.today()  # Current day to collect updated data
        historical_data = pd.get_data_yahoo(self.labels,  # Collects data from yahoo finance into a pandas dataframe
                                            start="2010-01-01",
                                            end=today)
        stats = historical_data['Adj Close'].pct_change()

        return stats.mean(), stats.cov()

    def portfolio_variables(self, weights, asset_average, cov_table):

        weights = np.array(weights)
        yields = np.sum(asset_average * weights) * self.TradingDays * 100
        standard_deviation = np.sqrt(np.dot(np.dot(weights, cov_table), weights.T)) * np.sqrt(self.TradingDays) * 100
        return np.array([yields, standard_deviation])

    def efficient_frontier(self, asset_average, cov_table):
        # Investment should be only on portfolios on this line:
        # under it you will have less yield for the same volatility, right of it more volatility for the same yield.

        bounds = tuple((0, 1) for i in range(self.A))
        init = [1 / self.A for i in range(self.A)]

        def returns(weights):
            return self.portfolio_variables(weights, asset_average, cov_table)[0]

        def volatility(weights):
            return self.portfolio_variables(weights, asset_average, cov_table)[1]

        for i in self.frontierY:
            cons = [{'type': 'eq', 'fun': lambda x: returns(x) - i},
                    {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}]

            result = sci.minimize(volatility, init, method='SLSQP',
                                  bounds=bounds, constraints=cons)
            self.frontierX.append(result['fun'])

    def display_simulation(self, sh_x, sh_y, min_x, min_y):  # Scatter graph (x = volatility, y = yield)

        plt.style.use('seaborn')
        plt.figure(figsize=(20, 10))
        plt.scatter(self.portfolios[0, :], self.portfolios[1, :], c=self.portfolios[2, :],
                    marker='o', s=10, alpha=0.5, cmap='plasma')
        plt.suptitle('Capitalized Asset Pricing Model', fontsize=25)
        plt.xlabel('Annualised Volatility in %', fontsize=15)
        plt.ylabel('Annualised Yield in %', fontsize=15)
        plt.plot(self.frontierX, self.frontierY, '--', linewidth=2, color='black', label='Efficient Frontier')
        plt.scatter(sh_x, sh_y, marker='o', color='grey', s=100, label='Maximum Sharpe Ratio')
        plt.scatter(min_x, min_y, marker='o', color='brown', s=100, label='Minimum Volatility')
        plt.legend(fontsize=15)
        # mng = plt.get_current_fig_manager()
        # mng.window.state('zoomed')
        plt.show()

    def portfolios_allocation(self, optimal_portfolio, safest_portfolio, sh_x, sh_y, min_x, min_y):  # Donut charts

        plt.style.use('fivethirtyeight')
        explode = []
        for i in range(self.A):
            explode.append(0.01)

        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(20, 10))
        axes[0].pie(optimal_portfolio, labels=self.labels, autopct='%1.1f%%', wedgeprops=dict(width=.36),
                    startangle=90, pctdistance=0.85, labeldistance=1.03, explode=explode)
        axes[0].axis('equal')
        axes[0].set_title('Optimal Stock Allocation', fontsize=25)
        axes[0].text(0.5, -0.1, 'Yield: ' + str(round(sh_y, 2)) + ' %\nVolatility: ' + str(round(sh_x, 2)) + ' %',
                     size=12, ha="center", transform=axes[0].transAxes, fontsize=15)

        axes[1].pie(safest_portfolio, labels=self.labels, autopct='%1.1f%%', wedgeprops=dict(width=.36),
                    startangle=90, pctdistance=0.85, labeldistance=1.03, explode=explode)
        axes[1].axis('equal')
        axes[1].set_title('Safest Stock Allocation', fontsize=25)
        axes[1].text(0.5, -0.1, 'Yield: ' + str(round(min_y, 2)) + ' %\nVolatility: ' + str(round(min_x, 2)) + ' %',
                     size=12, ha="center", transform=axes[1].transAxes, fontsize=15)
        plt.tight_layout()
        # mng = plt.get_current_fig_manager()
        # mng.window.state('zoomed')
        plt.show()


if __name__ == "__main__":

    tickers = []
    print("\nInsert number of assets in your portfolio: ")
    n_assets = int(input())

    print("\nInsert tickers of the assets: ")
    for t in range(n_assets):
        tickers.append(str(input()))
    print("\nBuilding simulation and calculating optimal portfolio...")

    p = Portfolio(n_assets, tickers)
    p.build_simulation()     # Results will be computed in %
