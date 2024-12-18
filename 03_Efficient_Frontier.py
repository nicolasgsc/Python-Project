import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load daily returns
data_file = 'portfolio_data_last_5_years.csv'
financial_data = pd.read_csv(data_file, index_col=0, parse_dates=True)
daily_returns = financial_data.pct_change().dropna()

# Define stocks
stocks = list(daily_returns.columns)

# Number of portfolio simulations (increased for better diversity)
num_portfolios = 100000

# Initialize arrays to store results
portfolio_returns = []
portfolio_volatilities = []
portfolio_sharpe_ratios = []
portfolio_weights = []

# Simulate portfolios
for _ in range(num_portfolios):
    # Generate random weights
    weights = np.random.random(len(stocks))
    weights /= np.sum(weights)  # Normalize weights
    portfolio_weights.append(weights)

    # Portfolio return
    portfolio_return = np.sum(daily_returns.mean() * weights) * 252
    portfolio_returns.append(portfolio_return)

    # Portfolio volatility
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(daily_returns.cov() * 252, weights)))
    portfolio_volatilities.append(portfolio_volatility)

    # Portfolio Sharpe Ratio
    sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_volatility
    portfolio_sharpe_ratios.append(sharpe_ratio)
# Convert results to DataFrame
portfolio_metrics = pd.DataFrame({
    'Return': portfolio_returns,
    'Volatility': portfolio_volatilities,
    'Sharpe Ratio': portfolio_sharpe_ratios
})

# Add weights to the DataFrame
for i, stock in enumerate(stocks):
    portfolio_metrics[stock + ' Weight'] = [w[i] for w in portfolio_weights]

# Identify optimal portfolios
max_sharpe_idx = portfolio_metrics['Sharpe Ratio'].idxmax()  # Maximum Sharpe Ratio
min_vol_idx = portfolio_metrics['Volatility'].idxmin()       # Minimum Volatility

optimal_sharpe = portfolio_metrics.iloc[max_sharpe_idx]
optimal_volatility = portfolio_metrics.iloc[min_vol_idx]

# Print optimal portfolios
print("\nPortfolio with Maximum Sharpe Ratio:")
print(optimal_sharpe)

print("\nPortfolio with Minimum Volatility:")
print(optimal_volatility)

# Plot the Efficient Frontier
plt.figure(figsize=(10, 6))
plt.scatter(portfolio_metrics['Volatility'], portfolio_metrics['Return'], c=portfolio_metrics['Sharpe Ratio'], cmap='viridis', alpha=0.7)
plt.colorbar(label='Sharpe Ratio')
plt.scatter(optimal_sharpe['Volatility'], optimal_sharpe['Return'], color='red', label='Max Sharpe Ratio', edgecolors='black')
plt.scatter(optimal_volatility['Volatility'], optimal_volatility['Return'], color='blue', label='Min Volatility', edgecolors='black')
plt.title('Efficient Frontier')
plt.xlabel('Volatility (Risk)')
plt.ylabel('Return')
plt.legend()

