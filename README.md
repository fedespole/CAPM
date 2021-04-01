# CAPM

CAPM is a financial model used to mitigate systematic risk through a correct asset allocation strategy.
It simulates several portfolios and selects the one with better yield/risk ratio.

Given as input a list of assets (in the form of tickers), the program:

- Downloads historical asset data from yahoo_finance using pandas_datareader, selecting mean returns and covariance matrices.
- Downloads the 3 Month US Treasury Bill Rate that is used as the risk free rate in the model.
- Generates random weights to build thousands of different portofolios.
- Computes the yield, the standard deviation and the Sharpe ratio of each of them, saving them as 3 attributes of each portfolio.
- Among the array of portfolios:
   * Selects the most performant portofolio (according to Willam Sharpe's theory), choosing the one with the highest Sharpe ratio.
   * Selects the safest portfolio, choosing the one with lowest volatility.
- Defines the efficient frontier of the portfolios using the scipy_minimize function with the proper constraints as argument. 
- Displays the simulation through a matplotlib scatter plot (x=volatility, y=yield).
- Displays donut charts of the selected portfolios, specifying the optimal distribution of the investments among the assets given.
