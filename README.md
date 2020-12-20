# CAPM

CAPM is a financial model developed by Sharpe and Markowitz, along with other mathematicians and economists. 
In a simplified and theoretical market, an investor faces two main risks: systemic and systematic. While the first one is inevitable as the trend of the stock market is influenced by the conditions of the economic system, the second one can be managed through diversification, and CAPM is one way to deal with it, because it describes the relationship between systematic risk and expected return for assets using the beta coefficient, and classifies the portofolios through the Sharpe ratio that is the correlation between (yield - risk free rate) and standard deviation.

Given as input a list of assets (in the form of tickers), the program:

- Downloads historical asset data from yahoo_finance using pandas_datareader, selecting mean returns and covariance matrices.
- Downloads the 3 Month US Treasury Bill Rate that is used as the risk free rate in the model.
- Generates random weights to build thousands of different portofolios.
- Computes the yield, the standard deviation and the Sharpe ratio of each of them, saving them as 3 attributes of each portfolio.
- Among the array of portfolios:
   > Selects the most performant portofolio (according to Willam Sharpe's theory) choosing the one with the highest Sharpe ratio.
   > Selects the safest portfolio choosing the one with lowest volatility.
- Defines the efficient frontier of the portfolios using the scipy_minimize function with the proper constraints as argument. 
- Displays the simulation through a matplotlib scatter plot (x=volatility, y=yield).
- Displays donut charts of the selected portfolios, specifying the optimal distribution of the investments among the assets given.
