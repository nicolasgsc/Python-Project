import numpy as np
import matplotlib.pyplot as plt

#############################
# 4. ES Computation & Feasibility Check
#############################

def portfolio_daily_return_series(daily_returns, weights):
    return (daily_returns * weights).sum(axis=1)

def compute_es(portfolio_daily_returns, confidence_level=0.95):
    """
    Compute the Expected Shortfall (ES) at a given confidence level.
    ES is the average return of the worst (1 - confidence_level)*100% of days.
    """
    sorted_returns = np.sort(portfolio_daily_returns)
    cutoff_index = int((1 - confidence_level) * len(sorted_returns))
    tail_losses = sorted_returns[:cutoff_index+1]
    es = tail_losses.mean()
    return es

# User inputs: portfolio size, confidence level, and max drawdown (in dollars)
try:
    portfolio_size = float(input("Enter your total portfolio size in dollars: "))
    confidence_level = float(input("Enter your desired confidence level for ES (e.g., 0.95 for 95%): "))
    max_drawdown_dollars = float(input("Enter the maximum dollar drawdown (ES) you are willing to accept: "))
except:
    print("Invalid input. Using defaults: portfolio_size=100000, confidence_level=0.95, max_drawdown_dollars=5000.")
    portfolio_size = 100000.0
    confidence_level = 0.95
    max_drawdown_dollars = 5000.0

# Compute ES for each portfolio and convert to dollar terms
es_list = []
for i in range(len(portfolio_metrics)):
    w = []
    for stock in stocks:
        w.append(portfolio_metrics.iloc[i][stock + ' Weight'])
    w = np.array(w)
    
    p_returns = portfolio_daily_return_series(daily_returns, w)
    es = compute_es(p_returns, confidence_level=confidence_level)
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
else:
    print("No portfolio meets the given ES dollar loss constraints.")
    optimal_portfolio = None

# Save feasible portfolios
feasible_portfolios.to_csv("feasible_portfolios.csv", index=False)
print("Feasible portfolios saved to 'feasible_portfolios.csv'.")


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

plt.title('Efficient Frontier with ES Constraints')
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
