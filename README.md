# Python Project: Portfolio Optimization Based on Investors' Maximum Accepted Drawdown, Using Monthly Expected Shortfall
# Background:
Investing can be a stressful endeavour. While the positive stock market return expectation is not only broadly known but also scientifically documented (see Dimson et al. 2002), many potential investors shy away from the potential risks and fail to benefit from the economic miracle public markets provide. Other investors pay large fees to financial advisors to reduce the volatility of their portfolios. What if individuals could specify their: publicly traded securities and risk tolerance to obtain tailor-made portfolio weightings in line with their risk appetite?

# Solution: 
Our Python program equips individual investors with the power to choose their optimal asset weightings based on Markowitz (1952) portfolio selection. We achieve this by combining Markowitz portfolio optimization with the concept of expected shortfall (ES). ES is the amount of money an investor stands to lose given an extreme (negative) event in public markets occurs. It is defined as a risk measure used to estimate the average loss of an investment portfolio in the worst-case scenario beyond a specified confidence level. To do this we assume historical returns to be reliable predictors of future returns when observing a reasonably long past time horizon, specified as at least 3 years. The trade-off was chosen to not exclude too many firms and funds that recently began trading and still obtain reliable statistical results. 

# How to run: 
The python scripts run well in jupyter notebook, it is necessary to run the programs in the prespecified order to ensure that the stored csv files from the previous program are available for the next.

# Functionality:
**01_Get_Financial_Data:**
The program retrieves historical stock prices and calculates an equal-weighted investment portfolio. It prompts the user to input up to 20 stock tickers from Yahoo Finance, validating each ticker's historical data availability and ensuring at least 3 years of trading history. The program calculates equal portfolio weights based on the number of valid stocks and fetches adjusted closing prices for each selected stock. After processing, the cleaned data is saved to a CSV file named 'portfolio_data_last_5_years.csv'. Additionally, the program retrieves the current U.S. Treasury Bill rate (^IRX) as the risk-free rate, displaying it or defaulting to 0% if retrieval fails.
The program returns the head and tails of selected assets and the risk-free rate obtained.

**02_Basic_Stats:**
The second program analyzes financial stock data by computing key performance metrics. It first loads historical price data from a CSV file. Daily returns are calculated to assess stock performance. Key metrics such as mean daily return, annualized return, volatility, and Sharpe ratio are computed for each stock. The program then aggregates these metrics into a comprehensive summary.
For the portfolio, daily and cumulative returns are calculated based on predefined weights. Annualized return, volatility, and the portfolio's Sharpe ratio are also determined. The results, including individual stock metrics and portfolio returns, are saved to CSV files for further analysis.
The program returns the first lines of calculated returns as well as summary statistics such as average daily returns and volatility which are also displayed annualized as well as the sharpe ratio of each asset. On portfolio level the annual return, volatility and sharpe ration are extracted.

**03_Efficient_Frontier:**
The third program performs a Monte Carlo simulation to identify optimal investment portfolios based on historical stock data. It loads daily returns from the CSV file created in 01 and uses random weight allocations to simulate 100,000 portfolios. For each portfolio, it calculates expected annual returns, volatility (risk), and the Sharpe ratio, considering a risk-free rate. The program stores these metrics and identifies portfolios with the maximum Sharpe ratio and minimum volatility. Finally, it visualizes the Efficient Frontier using a scatter plot, highlighting the optimal portfolios for risk-return trade-off analysis.

<img width="838" alt="image" src="https://github.com/user-attachments/assets/1cbbddee-6a17-413e-988a-a9e6c0966bc9" />

**04_Efficient_Frontier_with_ES_max_drawdown:**
The program performs Expected Shortfall (ES) analysis for investment portfolios using historical stock returns. It prompts the user for portfolio size, desired confidence level, and maximum acceptable monthly drawdown. The program calculates ES by averaging the worst-performing monthly returns at the specified confidence level. It filters portfolios meeting the ES constraint and selects the one with the highest return. Visual outputs include the Efficient Frontier with feasible portfolios highlighted and the optimal portfolio's weights shown in a pie chart. Portfolio metrics and feasible portfolios are saved to CSV files for further analysis.

<img width="891" alt="image" src="https://github.com/user-attachments/assets/f2fcb37e-2d3e-4d8d-bdfc-2e29c53dd5fd" />

# Portfolio weights example (GOOG, VB, NFLX, AAPL, URTH, MME=F)

<img width="628" alt="image" src="https://github.com/user-attachments/assets/41445903-d255-4187-aa9c-cce9f8ee7706" />


# Disclaimer: 
1) The program might have extensive run time due to the high number of portfolios being simulated.
2) For certain asset selection and risk specification there might be no feasible portfolio available, this is not a coding mistake but simply down to the risk-return characteristics of the included assets. In case your assets do not match your risk tolerance, please consider including less risky assets in your portfolio.
3) Our strong assumption of historical returns being representative for future returns requires us to have a minimum amount of data for each asset. We specified this to be at least 3 years, therefore any asset with less than 3 years of trading history cannot be used in our portfolio optimizer.

Sources: 
Dimson et al. (2002): https://www.researchgate.net/publication/248160012_Triumph_of_the_optimists_101_years_of_global_investment_returns

Markowitz (1952): https://www.jstor.org/stable/2975974


