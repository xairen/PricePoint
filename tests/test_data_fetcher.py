from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import os
from dotenv_vault import load_dotenv

load_dotenv()

# Replace 'YOUR_API_KEY' with your actual Alpha Vantage API key
api_key = os.getenv(API_KEY)

# Initialize the TimeSeries class with your API key
ts = TimeSeries(key=api_key, output_format='pandas')

# Get daily stock data for a specific symbol (e.g., 'AAPL' for Apple Inc.)
data, meta_data = ts.get_daily(symbol='AAPL', outputsize='compact')

# Plot the closing prices
data['4. close'].plot()
plt.title('Daily Closing Price for AAPL')
plt.show()