import datetime
import pandas as pd
import yfinance as yf

## 1. Set parameters

# Calculate the start date as 5 years from today
end_Date = datetime.date.today()
start_Date = end_Date - datetime.timedelta(days=5*365)

# List of stocks to analyze
stocks = ['AAPL', 'TSLA', 'MSFT', 'AMZN', 'GOOG']

# Define portfolio weights (equal weight in this case)
portfolio_weights = {stock: 1/len(stocks) for stock in stocks}

print("Portfolio Weights:")
for stock, weight in portfolio_weights.items():
    print(f"{stock}: {weight:.2%}")

## 2. Fetch the data

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

except Exception as e:
    # Print error message and exit
    print(f"Error fetching data: {e}")
    exit()

## 3. Structure the data

# Drop rows where all stock prices are NaN
all_data.dropna(how="all", inplace=True)

# Drop columns (stocks) that have only NaN values
all_data.dropna(axis=1, how="all", inplace=True)

# Ensure all data is aligned and consistent
all_data.index = all_data.index.tz_localize(None)  # Remove timezone if present

## 4. Save data

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
