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
num_portfolios = 10000

# Risk-free rate (assumed for Sharpe Ratio)
risk_free_rate = 0.01

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

# Dynamically adjust the maximum allowed volatility
max_allowed_volatility = max(portfolio_metrics['Volatility'].max(), 1.0)

# Validate user input for risk tolerance
while True:
    try:
        max_risk = float(input(f"\nEnter your maximum acceptable risk (volatility, 0 to {max_allowed_volatility:.2f}): "))
        if max_risk <= 0 or max_risk > max_allowed_volatility:
            print(f"Please enter a value between 0 and {max_allowed_volatility:.2f}. Typical values are between 0.1 and 0.4.")
            continue
        break
    except ValueError:
        print("Invalid input. Please enter a valid number.")

# Filter portfolios with volatility less than or equal to the user's input
filtered_portfolios = portfolio_metrics[portfolio_metrics['Volatility'] <= max_risk]

if not filtered_portfolios.empty:
    # Find the portfolio with the highest return under the risk constraint
    user_optimal_portfolio = filtered_portfolios.loc[filtered_portfolios['Return'].idxmax()]
    print("\nOptimal Portfolio for your Risk Tolerance:")
    print(user_optimal_portfolio)

    # Highlight this portfolio on the plot
    plt.scatter(user_optimal_portfolio['Volatility'], user_optimal_portfolio['Return'], color='green', label='User Optimal Portfolio', edgecolors='black')
    plt.legend()
    plt.show()

    # Save user optimal portfolio to CSV
    user_optimal_portfolio.to_frame().T.to_csv('user_optimal_portfolio.csv')
    print("User optimal portfolio saved to 'user_optimal_portfolio.csv'.")
else:
    print("\nNo portfolios found within the specified risk tolerance.")
    plt.show()
