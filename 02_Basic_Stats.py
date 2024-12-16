import pandas as pd
import numpy as np

## 1. Load financial data

# Load the financial data from the previous step
data_file = 'portfolio_data_last_5_years.csv'
financial_data = pd.read_csv(data_file, index_col=0, parse_dates=True)

## 2. Compute daily returns for each stock

# Calculate daily percentage changes (returns)
daily_returns = financial_data.pct_change().dropna()

print("\nDaily Returns (Head):")
print(daily_returns.head())

## 3. Compute key metrics for each stock

# Mean daily return
mean_daily_return = daily_returns.mean()

# Annualized return
annualized_return = mean_daily_return * 252

# Volatility (standard deviation of daily returns, annualized)
daily_volatility = daily_returns.std()
annualized_volatility = daily_volatility * np.sqrt(252)

# Sharpe ratio for each stock (assuming risk-free rate = 0)
sharpe_ratios = annualized_return / annualized_volatility

# Combine metrics into a DataFrame
metrics = pd.DataFrame({
    'Mean Daily Return': mean_daily_return,
    'Annualized Return': annualized_return,
    'Daily Volatility': daily_volatility,
    'Annualized Volatility': annualized_volatility,
    'Sharpe Ratio': sharpe_ratios
})

print("\nMetrics for Individual Stocks:")
print(metrics)

## 4. Compute portfolio metrics

# Aggregate portfolio daily returns based on weights
portfolio_daily_return = daily_returns.dot(pd.Series(portfolio_weights))

# Portfolio cumulative return
portfolio_cumulative_return = (1 + portfolio_daily_return).cumprod()

# Portfolio annualized return
portfolio_annualized_return = portfolio_daily_return.mean() * 252

# Portfolio volatility
portfolio_volatility = portfolio_daily_return.std() * np.sqrt(252)

# Portfolio Sharpe Ratio (assuming risk-free rate = 0)
portfolio_sharpe_ratio = portfolio_annualized_return / portfolio_volatility

# Combine portfolio metrics into a summary
portfolio_metrics = {
    'Annualized Return': portfolio_annualized_return,
    'Volatility': portfolio_volatility,
    'Sharpe Ratio': portfolio_sharpe_ratio
}

print("\nPortfolio Metrics:")
for key, value in portfolio_metrics.items():
    print(f"{key}: {value:.2%}")

## 5. Save results to CSV

# Save individual stock metrics
metrics.to_csv('individual_stock_metrics.csv')
print("\nMetrics for individual stocks saved to 'individual_stock_metrics.csv'.")

# Save portfolio daily and cumulative returns
portfolio_returns = pd.DataFrame({
    'Portfolio Daily Return': portfolio_daily_return,
    'Portfolio Cumulative Return': portfolio_cumulative_return
})
portfolio_returns.to_csv('portfolio_returns.csv')
print("Portfolio returns saved to 'portfolio_returns.csv'.")

