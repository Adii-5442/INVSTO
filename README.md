# INVSTO : Stock Analysis and Trading Strategy 

This Python script is designed for stock data analysis and the creation of a simple moving average (SMA) crossover trading strategy. It includes data insertion into a MySQL database, data fetching, and performance analysis of the trading strategy.

<div align="center" style="display: flex; justify-content: center; align-items: center;marginTop:50">
  <img src="/performance.png" alt="Performance">
</div>


## Usage

1. **Data Insertion**: The script inserts stock data from a CSV file (`data.csv`) into a MySQL database. Make sure you have a MySQL server running with the necessary database configuration (specified in `db_params`).

2. **Data Fetching**: The `fetch` function retrieves the data from the MySQL database for analysis. Ensure that you have successfully inserted data before running analysis.

3. **Trading Strategy**: The script implements a simple moving average crossover trading strategy. It calculates the SMA50 and SMA200, generates buy/sell signals, and computes returns.

4. **Performance Metrics**: The `ReturnsCalc` function calculates various trading performance metrics, including total return, maximum drawdown, Sharpe ratio, and win-loss ratio.

5. **Unit Tests**: The code includes unit tests to check the validity of the fetched data and the correctness of the trading strategy calculations.

## Configuration

- Modify the `db_params` dictionary to match your MySQL database configuration.
- Adjust the `initial_investment` value in the `ReturnsCalc` function to represent your initial investment.

## Running the Script

```bash
python main.py
```

## Requirements

Before using this code, ensure you have the following Python packages installed:

- `mysql-connector-python`: To interact with the MySQL database.
- `pandas`: For data manipulation and analysis.
- `numpy`: For numerical operations.
- `unittest`: For running unit tests.
- `datetime`: For working with date and time data.

You can install these packages using `pip`:

```bash
pip install mysql-connector-python pandas numpy
