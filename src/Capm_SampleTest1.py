from src import capm_model

n_assets = 5
# ex: Tech companies: ibm, intel, google, cisco, facebook
tickers = ['IBM', 'INTC', 'GOOGL', 'CSCO', 'FB']

print("\nBuilding simulation and calculating optimal portfolio...")

p = CAPM.Portfolio(n_assets, tickers)
p.build_simulation()    # Results will be computed in %
