import yfinance as yf
import pandas as pd
import numpy as np
import datetime
import sys

## 1. Set parameters

# Calculate the start date as 5 years from today
end_Date = pd.Timestamp(datetime.date.today())
start_Date = end_Date - pd.DateOffset(years=5)

def get_valid_tickers():
    tickers = []
    print("Please enter up to 50 valid stock tickers from Yahoo Finance.")
    while len(tickers) < 50:
        user_input = input(f"Enter ticker {len(tickers)+1} (or press Enter to finish): ").upper().strip()
        if user_input == "":
            if len(tickers) > 1:
                break
            else:
                print("You must enter at least two ticker.")
                continue
        
        if user_input in tickers:
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

# Drop rows where all stock prices are NaN
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
    risk_free_ticker = yf.Ticker("^IRX")
    risk_free_data = risk_free_ticker.history(period="1d")
    risk_free_rate = risk_free_data['Close'].iloc[-1] / 100  # Convert from percentage to decimal
    print(f"\nCurrent Risk-Free Rate: {risk_free_rate:.2%}")
except Exception as e:
    print(f"Error fetching risk-free rate: {e}")
    risk_free_rate = 0.0
