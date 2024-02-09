from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import os
from dotenv_vault import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")

def plot_stocks(stock_symbols, api_key, outputsize='compact'):
    ts = TimeSeries(key=api_key, output_format='pandas')

    for symbol in stock_symbols:
        try:
            #Get daily stock data for current symbol
            data, met_data = ts.get_daily(symbol=symbol, outputsize=outputsize)

            #Plot the closing prices
            plt.figure(figsize=(10,6))
            data['4. close'].plot()
            plt.title(f'Daily Closing Price for {symbol}')
            plt.show()
        except Exception as e:
            print(f"Error while fetching data for {symbol}: {e}")

stock_symbols = ['AAPL', 'MSFT', 'GOOGL']

plot_stocks(stock_symbols, api_key)