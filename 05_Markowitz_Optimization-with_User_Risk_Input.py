import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.optimize as sco

# Load daily returns
data_file = 'portfolio_data_last_5_years.csv'
financial_data = pd.read_csv(data_file, index_col=0, parse_dates=True)
daily_returns = financial_data.pct_change().dropna()

# Define stocks
stocks = list(daily_returns.columns)

# Risk-free rate (assumed for Sharpe Ratio)
risk_free_rate = 0.01

# Calculate mean returns and covariance matrix
mean_returns = daily_returns.mean()
cov_matrix = daily_returns.cov()

# Function to calculate portfolio volatility (risk)
def portfolio_volatility(weights, mean_returns, cov_matrix):
    return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

# Function to calculate portfolio return
def portfolio_return(weights, mean_returns):
    return np.sum(mean_returns * weights)

# Function to ensure weights sum to 1
def check_sum(weights):
    return np.sum(weights) - 1

# Get user input for risk tolerance (maximum volatility)
while True:
    try:
        max_risk = float(input(f"\nEnter your maximum acceptable risk (volatility, 0 to 1.0): "))
        if max_risk <= 0 or max_risk > 1.0:
            print(f"Please enter a value between 0 and 1.0. Typical values are between 0.1 and 0.4.")
            continue
        break
    except ValueError:
        print("Invalid input. Please enter a valid number.")

# Simulate portfolios to find the one with the highest return under the risk constraint (max volatility)
num_portfolios = 10000
portfolio_returns = []
portfolio_volatilities = []
portfolio_weights = []

for _ in range(num_portfolios):
    weights = np.random.random(len(stocks))
    weights /= np.sum(weights)  # Normalize weights

    # Calculate portfolio return
    port_return = portfolio_return(weights, mean_returns)
    portfolio_returns.append(port_return)

    # Calculate portfolio volatility
    port_volatility = portfolio_volatility(weights, mean_returns, cov_matrix)
    portfolio_volatilities.append(port_volatility)

    # Save the portfolio weights
    portfolio_weights.append(weights)

# Create a DataFrame for portfolio results
portfolio_metrics = pd.DataFrame({
    'Return': portfolio_returns,
    'Volatility': portfolio_volatilities
})

# Filter portfolios to get those within the max risk (volatility) constraint
filtered_portfolios = portfolio_metrics[portfolio_metrics['Volatility'] <= max_risk]

if not filtered_portfolios.empty:
    # Find the portfolio with the highest return under the risk constraint
    optimal_portfolio = filtered_portfolios.loc[filtered_portfolios['Return'].idxmax()]
    print("\nOptimal Portfolio for your Risk Tolerance:")
    print(optimal_portfolio)

    # Visualize the Efficient Frontier
    plt.figure(figsize=(10, 6))
    plt.scatter(portfolio_metrics['Volatility'], portfolio_metrics['Return'], c=portfolio_metrics['Return'], cmap='viridis', alpha=0.7)
    plt.colorbar(label='Return')
    plt.scatter(optimal_portfolio['Volatility'], optimal_portfolio['Return'], color='green', label='User Optimal Portfolio', edgecolors='black')
    plt.title('Efficient Frontier with User Risk Tolerance')
    plt.xlabel('Volatility (Risk)')
    plt.ylabel('Return')
    plt.legend()
    plt.show()

    # Save optimal portfolio metrics to CSV
    optimal_portfolio.to_frame().T.to_csv('user_optimal_portfolio.csv')
    print("User optimal portfolio saved to 'user_optimal_portfolio.csv'.")
else:
    print("\nNo portfolios found within the specified risk tolerance.")
    plt.show()

# Markowitz Optimization: Find the portfolio that gives the maximum return for a given risk
def optimize_portfolio(mean_returns, cov_matrix, max_risk):
    num_assets = len(mean_returns)
    initial_guess = num_assets * [1. / num_assets]  # Equal distribution as a starting point
    bounds = tuple((0, 1) for asset in range(num_assets))  # All weights must be between 0 and 1
    constraints = ({'type': 'eq', 'fun': check_sum})  # Sum of weights must be 1

    # Minimize the portfolio volatility
    result = sco.minimize(portfolio_volatility, initial_guess, args=(mean_returns, cov_matrix), method='SLSQP', bounds=bounds, constraints=constraints)

    return result.x  # Optimal weights

# Find the optimal portfolio
optimal_weights = optimize_portfolio(mean_returns, cov_matrix, max_risk)
print("\nOptimal Portfolio Weights (Max Return for a Given Risk):")
print(optimal_weights)

# Show optimal portfolio weights in a pie chart
plt.figure(figsize=(8, 8))
plt.pie(optimal_weights, labels=stocks, autopct='%1.1f%%', startangle=140)
plt.title("Optimal Portfolio Weights (Max Return for a Given Risk)")
plt.show()

# Save the optimal portfolio weights to a CSV
optimal_portfolio_df = pd.DataFrame(optimal_weights, index=stocks, columns=['Weight'])
optimal_portfolio_df.to_csv('optimal_portfolio_weights.csv')
print("Optimal portfolio weights saved to 'optimal_portfolio_weights.csv'.")
