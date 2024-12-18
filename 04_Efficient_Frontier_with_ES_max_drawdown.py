import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def portfolio_monthly_return_series(daily_returns, weights):
    portfolio_daily_returns = (daily_returns * weights).sum(axis=1)
    monthly_returns = portfolio_daily_returns.resample('M').sum()
    return monthly_returns

def compute_es(portfolio_returns, confidence_level=0.95):
    """
    Compute the Expected Shortfall (ES) at a given confidence level.
    ES is the average return of the worst (1 - confidence_level)*100% of months.
    """
    sorted_returns = np.sort(portfolio_returns)
    cutoff_index = int((1 - confidence_level) * len(sorted_returns))
    tail_losses = sorted_returns[:cutoff_index+1]
    es = tail_losses.mean()
    return es

# Prompt for portfolio size
while True:
    try:
        portfolio_size = float(input("Enter your total portfolio size in dollars: "))
        if portfolio_size <= 0:
            print("Portfolio size must be greater than 0.")
            continue
        break
    except ValueError:
        print("Invalid input. Please enter a numeric value.")

# Prompt for confidence level
while True:
    try:
        confidence_level = float(input("Enter your desired confidence level for ES (0 < confidence_level < 1, e.g., 0.95): "))
        if confidence_level <= 0 or confidence_level >= 1:
            print("Confidence level must be between 0 and 1.")
            continue
        break
    except ValueError:
        print("Invalid input. Please enter a numeric value.")

# Prompt for maximum drawdown
while True:
    try:
        max_drawdown_dollars = float(input("Enter the maximum monthly drawdown (ES) you are willing to accept in dollars: "))
        if max_drawdown_dollars <= 0:
            print("Maximum drawdown must be greater than 0.")
            continue
        if max_drawdown_dollars >= portfolio_size:
            print("Maximum drawdown must be smaller than the portfolio size.")
            continue
        break
    except ValueError:
        print("Invalid input. Please enter a numeric value.")

# If we reach this point, all values have been validated
print("\nInputs validated successfully:")
print(f"Portfolio Size: {portfolio_size}")
print(f"Confidence Level: {confidence_level}")
print(f"Max Monthly Drawdown (Dollars): {max_drawdown_dollars}")

# Compute ES for each portfolio and convert to dollar terms
es_list = []
for i in range(len(portfolio_metrics)):
    w = []
    for stock in stocks:
        w.append(portfolio_metrics.iloc[i][stock + ' Weight'])
    w = np.array(w)
    
    monthly_returns = portfolio_monthly_return_series(daily_returns, w)
    es = compute_es(monthly_returns, confidence_level=confidence_level)
    es_list.append(es)

portfolio_metrics['ES'] = es_list
portfolio_metrics['ES_dollars'] = portfolio_metrics['ES'] * portfolio_size


# Filter portfolios to those that meet the user's ES dollar threshold
feasible_portfolios = portfolio_metrics[portfolio_metrics['ES_dollars'] >= (-max_drawdown_dollars)]

# Among feasible portfolios, choose the one with the highest return
if not feasible_portfolios.empty:
    optimal_portfolio = feasible_portfolios.loc[feasible_portfolios['Return'].idxmax()]
    print("\nOptimal portfolio that meets the ES constraints (from feasible set):")
    print(optimal_portfolio)

    print("\nOptimal Portfolio Weights:")
    for stock in stocks:
        print(f"{stock}: {optimal_portfolio[stock + ' Weight']:.2%}")
    
    print(f"\nAnnualized Return: {optimal_portfolio['Return']:.2%}")
    print(f"Volatility: {optimal_portfolio['Volatility']:.2%}")
    print(f"ES (as fraction): {optimal_portfolio['ES']:.2%}")
    print(f"ES (in dollars): ${optimal_portfolio['ES_dollars']:.2f}")
    
    # Save feasible portfolios
    feasible_portfolios.to_csv("feasible_portfolios.csv", index=False)
    print("Feasible portfolios saved to 'feasible_portfolios.csv'.")
else:
    print("No portfolio meets the given ES dollar loss constraints.")
    optimal_portfolio = None

#############################################
# Plot the Efficient Frontier, Feasible Portfolios, and Highlight the Optimal Portfolio
#############################################

plt.figure(figsize=(10, 6))

# Plot all portfolios
plt.scatter(portfolio_metrics['Volatility'], portfolio_metrics['Return'], 
            color='blue', alpha=0.5, label='All Portfolios')

# Plot only the feasible portfolios (that meet the ES constraint)
if not feasible_portfolios.empty:
    plt.scatter(feasible_portfolios['Volatility'], feasible_portfolios['Return'], 
                color='orange', alpha=0.7, label='ES-Feasible Portfolios')

# Highlight the chosen feasible optimal portfolio on the plot
if optimal_portfolio is not None:
    plt.scatter(optimal_portfolio['Volatility'], optimal_portfolio['Return'], 
                color='green', s=120, edgecolors='black', 
                label='Feasible Optimal Portfolio')

plt.title('Efficient Frontier with ES Constraints (Monthly)')
plt.xlabel('Volatility (Std. Deviation)')
plt.ylabel('Annualized Return')
plt.legend()
plt.show()

# Plot the Portfolio Weights for the ES-optimal portfolio (if it exists)
if optimal_portfolio is not None:
    plt.figure(figsize=(8, 8))
    optimal_portfolio_weights = [optimal_portfolio[stock + ' Weight'] for stock in stocks]
    plt.pie(optimal_portfolio_weights, labels=stocks, autopct='%1.1f%%', startangle=140)
    plt.title("Portfolio Weights for the ES-Optimal Portfolio")
    plt.show()
