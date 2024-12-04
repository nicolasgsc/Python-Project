import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from scipy.stats import norm

# Define available stocks (30)
all_stocks = ['AAPL', 'TSLA', 'MSFT', 'AMZN', 'GOOG', 'META', 'NFLX', 'NVDA', 'IBM', 'AMD',
              'BA', 'DIS', 'PFE', 'NVDA', 'INTC', 'V', 'MA', 'PYPL', 'GE', 'KO',
              'JNJ', 'PEP', 'T', 'XOM', 'CVX', 'WMT', 'UNH', 'MCD', 'INTU', 'CRM']

# Display available stock tickers for selection
print("Available stocks:")
for i, stock in enumerate(all_stocks, 1):
    print(f"{i}. {stock}")

# User input to select stocks (up to 10)
selected_stocks = []
while len(selected_stocks) < 1 or len(selected_stocks) > 10:
    try:
        selected_stocks_input = input(f"\nEnter the stock numbers (separate by commas, up to 10 stocks): ")
        
        # Check for correct comma usage (not trailing commas, not missing commas)
        if ',' not in selected_stocks_input:
            print("Error: Please separate stock numbers with commas.")
            continue
        
        # Split the input by commas, strip any spaces, and ensure it's valid
        selected_numbers = [int(x.strip()) for x in selected_stocks_input.split(',')]
        
        # Ensure no more than 10 stocks are selected and no duplicate numbers
        if len(selected_numbers) > 10:
            print("Error: You can only select up to 10 stocks. Please try again.")
            continue
        if len(selected_numbers) != len(set(selected_numbers)):  # Check for duplicates
            print("Error: Duplicate stock numbers detected. Please choose unique numbers.")
            continue
        
        # Get the stock symbols from the selected numbers
        selected_stocks = [all_stocks[i - 1] for i in selected_numbers if 1 <= i <= len(all_stocks)]
        
        if not selected_stocks:
            print("Error: No valid stocks selected. Please try again.")
            continue
        
        break  # Break if the input is valid

    except ValueError:
        print("Error: Invalid input. Please enter valid stock numbers (e.g., 1, 2, 5).")
    except IndexError:
        print("Error: One or more of your stock selections were invalid. Please try again.")

# Load daily returns for the selected stocks
data_file = 'portfolio_data_last_5_years.csv'
financial_data = pd.read_csv(data_file, index_col=0, parse_dates=True)
daily_returns = financial_data[selected_stocks].pct_change().dropna()

# Define stocks
stocks = selected_stocks

# Risk-free rate (assumed for Sharpe Ratio)
risk_free_rate = 0.01

# Number of portfolio simulations (increased for better diversity)
num_portfolios = 10000

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
    portfolio_return = np.sum(daily_returns.mean() * weights) * 252  # Annualize return
    portfolio_returns.append(portfolio_return)

    # Portfolio volatility (annualized)
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(daily_returns.cov() * 252, weights)))  # Annualize volatility
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

# User Input for Value at Risk (VaR) and Expected Shortfall (ES)
confidence_level = float(input("\nEnter confidence level for VaR and ES (e.g., 95 for 95% confidence): "))
holding_period = float(input("\nEnter holding period in days (e.g., 1 for 1 day, 5 for 5 days, 30 for 30 days): "))

# Calculate VaR using the historical simulation method
VaR = -np.percentile(daily_returns.sum(axis=1), 100 - confidence_level)

# Scale VaR based on the holding period (assuming normal distribution)
VaR_scaled = VaR * np.sqrt(holding_period)

# Calculate Expected Shortfall (ES) and scale it by the holding period
ES = -daily_returns[daily_returns.sum(axis=1) <= -VaR].mean().sum()
ES_scaled = ES * np.sqrt(holding_period)

# Print VaR and ES with the holding period adjustment
print(f"\nValue at Risk (VaR) at {confidence_level}% confidence level for a {holding_period}-day holding period: {VaR_scaled:.2f}")
print(f"Expected Shortfall (ES) at {confidence_level}% confidence level for a {holding_period}-day holding period: {ES_scaled:.2f}")

# Plot the Portfolio Weights for the optimal portfolio (Pie chart for selected portfolio)
plt.figure(figsize=(8, 8))
optimal_portfolio_weights = portfolio_weights[max_sharpe_idx]  # Use max Sharpe Ratio portfolio for example
plt.pie(optimal_portfolio_weights, labels=stocks, autopct='%1.1f%%', startangle=140)
plt.title("Portfolio Weights for the Max Sharpe Ratio Portfolio")
plt.show()

