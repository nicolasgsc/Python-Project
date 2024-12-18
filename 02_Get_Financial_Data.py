import yfinance as yf
import pandas as pd
import numpy as np
import datetime
import sys

## 1. Set parameters

# Calculate the start date as 5 years from today
end_Date = pd.Timestamp(datetime.date.today())
start_Date = end_Date - pd.DateOffset(years=5)

def get_valid_tickers(): #Function to get up to 20 valid stock tickers from the user
    tickers = []
    print("Please enter up to 20 valid stock tickers from Yahoo Finance.")
    while len(tickers) < 20:
        user_input = input(f"Enter ticker {len(tickers)+1} (or press Enter to finish): ").upper().strip() 
        #The user is being prompted for a new ticker up to 20 tickers but can press enter to finish his selection after having selected 2 assets
        if user_input == "":
            if len(tickers) > 1:
                break
            else:
                print("You must enter at least two ticker.")
                continue
        
        if user_input in tickers: #The user can't enter the same ticker multiple times
            print(f"{user_input} has already been entered. Please enter a different ticker.")
            continue

        try:
            stock = yf.Ticker(user_input)
            stock_info = stock.info
            
            # Check if ticker is valid (has a shortName)
            if 'shortName' in stock_info and stock_info['shortName']:
                
                # Fetch up to 5 years of data for the ticker
                data = yf.download(user_input, start=start_Date, end=end_Date)['Adj Close']
                
                if data.empty:
                    print(f"{user_input} returned no data. Please try another ticker.")
                    continue

                # Calculate the available history for this ticker
                first_available_date = data.index[0]
                last_available_date = data.index[-1]
                years_of_history = (last_available_date - first_available_date).days / 365.25
                # Check if we have at least 3 years of data
                if years_of_history < 3:
                    print(f"{user_input} does not have at least 3 years of history (only {years_of_history:.2f} years). Please try another ticker.")
                    continue

                # If it passes all checks, append the ticker
                tickers.append(user_input)

            else:
                print(f"{user_input} is not a valid ticker. Please try again.")

        except Exception as e:
            print(f"Error fetching data for {user_input}: {e}. Please try again.")

    print(f"You have selected: {', '.join(tickers)}")
    return tickers

stocks = get_valid_tickers()

# Calculate equal weights dynamically (as starting portfolio weights)
num_stocks = len(stocks)
portfolio_weights = {stock: 1/num_stocks for stock in stocks}

print("Portfolio Weights:")
for stock, weight in portfolio_weights.items():
    print(f"{stock}: {weight:.2%}")

# Initialize an empty DataFrame to hold all stock data
all_data = pd.DataFrame()

try:
    print("\nFetching data for stocks...")
    for stock in stocks:
        # Download Adjusted Close Prices for the stock
        data = yf.download(stock, start=start_Date, end=end_Date)['Adj Close']
        if data.empty:
            print(f"Warning: No data found for {stock}. Skipping...")
        else:
            all_data[stock] = data
            print("Successfully loaded stock data")
except Exception as e:
    print(f"Error fetching data: {e}")
    sys.exit()
## 3. Structure the data

# Drop rows where all stock prices are NaN, this causes the whole dataset to be shortened when one of the assets is between 3 and 5 years old otherwise we get the whole 5 years of data

all_data.dropna(how="all", inplace=True)

# Drop columns (stocks) that have only NaN values
all_data.dropna(axis=1, how="all", inplace=True)

# Ensure all data is aligned and consistent
all_data.index = all_data.index.tz_localize(None)  # Remove timezone if present
if not all_data.empty:
    print("\nProcessed Data (Head):")
    print(all_data.head())

    print("\nProcessed Data (Tail):")
    print(all_data.tail())

    # Save the processed data to a CSV file
    output_file = 'portfolio_data_last_5_years.csv'
    all_data.to_csv(output_file, encoding='UTF-8')
    print(f"Data successfully saved to {output_file}")
else:
    print("No valid stock data available. Exiting...")

# Fetch current risk-free rate from Yahoo Finance
try:
    risk_free_ticker = yf.Ticker("^IRX") #Using the 13 week US treasury bill
    risk_free_data = risk_free_ticker.history(period="1d")
    risk_free_rate = risk_free_data['Close'].iloc[-1] / 100  # Convert from percentage to decimal
    print(f"\nCurrent Risk-Free Rate: {risk_free_rate:.2%}")
except Exception as e:
    print(f"Error fetching risk-free rate: {e}")
    risk_free_rate = 0.0 # In case we fail to specify the risk free rate via treasury bills we will assume a risk free interest rate of 0
    


"""Part 2"""
import pandas as pd
import numpy as np

## 1. Load financial data

# Load the financial data from the previous step
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

# Fetch current risk-free rate from Yahoo Finance
try:
    risk_free_ticker = yf.Ticker("^IRX")
    risk_free_data = risk_free_ticker.history(period="1d")
    risk_free_rate = risk_free_data['Close'].iloc[-1] / 100  # Convert from percentage to decimal
    print(f"\nCurrent Risk-Free Rate: {risk_free_rate:.2%}")
except Exception as e:
    print(f"Error fetching risk-free rate: {e}")
    risk_free_rate = 0.0

# Sharpe ratio for each stock
excess_return = annualized_return - risk_free_rate
sharpe_ratios = excess_return / annualized_volatility

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

## 5. Plot daily returns

import matplotlib.pyplot as plt
import numpy as np

plt.figure(figsize=(14, 7))

# Plot all individual stocks with transparency
for stock in daily_returns.columns:
    plt.plot(daily_returns[stock], alpha=0.3, linewidth=1, label=stock)

# Overlay the portfolio returns with higher line width and label
plt.plot(portfolio_daily_return, color='black', linewidth=2, label='Portfolio')

plt.title("Daily Returns: All Individual Stocks vs. Portfolio")
plt.xlabel("Date")
plt.ylabel("Daily Return")
plt.grid(True)
plt.legend(loc='upper right', ncol=2, fontsize='small')
plt.show()
