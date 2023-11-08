import mysql.connector
import pandas as pd
import numpy as np
import unittest
from datetime import datetime

db_params = {
    "host": "localhost",
    "user": "root",
    "password": "royalkludge",
    "database": "stock_table"
}
def insertDataToDB():
    conn = mysql.connector.connect(**db_params)
    data = pd.read_csv('data.csv')
    cursor = conn.cursor()
    insert_query = "INSERT INTO stock_data (datetime, close , high , low , open, volume , instrument) VALUES (%s, %s, %s, %s, %s, %s, %s)"

    for _, row in data.iterrows():
        cursor.execute(insert_query, (row['datetime'], row['close'], row['high'], row['low'], row['open'], row['volume'], row['instrument']))
    conn.commit()

insertDataToDB()

def fetch():
    conn = mysql.connector.connect(**db_params)
    query = "SELECT datetime, close, high, low, open, volume, instrument FROM stock_data;"
    data = pd.read_sql(query, conn)
    conn.close()
    return data

def SignalCalc(data):
    short_term_sma_period = 50
    long_term_sma_period = 200

    data['SMA50'] = data['close'].rolling(window=short_term_sma_period).mean()
    data['SMA200'] = data['close'].rolling(window=long_term_sma_period).mean()

    data['Signal'] = 0
    data['Signal'][short_term_sma_period:] = np.where(
        data['SMA50'][short_term_sma_period:] > data['SMA200'][short_term_sma_period:], 1, -1)

    return data

def ReturnsCalc(data):
    data['Return'] = data['close'].pct_change()
    data['Strategy_Return'] = data['Signal'].shift(1) * data['Return']
    data['Cumulative_Return'] = (1 + data['Strategy_Return']).cumprod()
    print(data)

    initial_investment = 10000
    final_portfolio_value = (1 + data['Strategy_Return']).prod() * initial_investment
    total_return = (final_portfolio_value - initial_investment) / initial_investment

    cumulative_returns = (1 + data['Strategy_Return']).cumprod()
    peak = cumulative_returns.cummax()
    drawdown = (cumulative_returns - peak) / peak
    max_drawdown = drawdown.min()

    risk_free_rate = 0
    daily_returns = data['Strategy_Return']
    sharpe_ratio = (daily_returns.mean() - risk_free_rate) / daily_returns.std()

    winning_trades = len(data[data['Strategy_Return'] > 0])
    losing_trades = len(data[data['Strategy_Return'] < 0])
    win_loss_ratio = winning_trades / losing_trades

    print("-------------------------------------------------------------------------")
    print("Total Return:\t\t\t", total_return)
    print("-------------------------------------------------------------------------")
    print("Maximum Drawdown:\t\t", max_drawdown)
    print("-------------------------------------------------------------------------")
    print("Sharpe Ratio:\t\t\t", sharpe_ratio)
    print("-------------------------------------------------------------------------")
    print("Win-Loss Ratio:\t\t\t", win_loss_ratio)
    print("-------------------------------------------------------------------------")

    return data

class TestStockAnalysis(unittest.TestCase):
    def setUp(self):
        self.data = fetch()

    def test_fetch(self):
        self.assertTrue(all(isinstance(value, float) for value in self.data['close']))
        self.assertTrue(all(isinstance(value, float) for value in self.data['high']))
        self.assertTrue(all(isinstance(value, float) for value in self.data['low']))
        self.assertTrue(all(isinstance(value, float) for value in self.data['open']))
        self.assertTrue(all(isinstance(value, int) for value in self.data['volume']))
        self.assertTrue(all(isinstance(value, str) for value in self.data['instrument']))
        self.assertTrue(all(isinstance(value, datetime) for value in self.data['datetime']))

        print("All Fetched data is Valid")

    def test_calc_signal(self):
        signalColumn = SignalCalc(self.data)
        self.assertTrue('SMA50' in signalColumn.columns)
        self.assertTrue('SMA200' in signalColumn.columns)
        self.assertTrue(all(signalColumn['Signal'].isin([-1, 0, 1])))

        print("All Signal data are in correct format")

    def test_return(self):
        signalColumn = SignalCalc(self.data)
        returnColumn = ReturnsCalc(signalColumn)
        self.assertTrue('Return' in returnColumn.columns)
        self.assertTrue('Strategy_Return' in returnColumn.columns)
        self.assertTrue('Cumulative_Return' in returnColumn.columns)

        print("Return Columns are in good shape")


if __name__ == '__main__':
    unittest.main()
