import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import os

# Configuration
from dotenv_vault import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")
symbol = 'AAPL'
window_size = 60  # Days of historical data to consider for each prediction
forecast_months = [1, 2, 3]  # Forecast 1, 2, and 3 months into the future
days_in_month = 20  # Average number of trading days in a month

# Fetch stock data
ts = TimeSeries(key=api_key, output_format='pandas')
data, _ = ts.get_daily(symbol=symbol, outputsize='full')
data = data['4. close'].iloc[::-1]  # Ensure chronological order

# Prepare data for model
def prepare_data(data, window_size, forecast_days):
    X, y = [], []
    for i in range(len(data) - window_size - forecast_days):
        X.append(data[i:(i + window_size)])
        y.append(data[i + window_size + forecast_days])
    return np.array(X), np.array(y)

# Model training and prediction function
def train_and_predict(data, window_size, forecast_day):
    X, y = prepare_data(data, window_size, forecast_day)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    model = LinearRegression()
    model.fit(X_train, y_train)
    prediction = model.predict([data[-window_size:]])
    return prediction[0]

# Main prediction loop
for months in forecast_months:
    forecast_days = days_in_month * months
    predicted_price = train_and_predict(data.values, window_size, forecast_days)
    print(f"Predicted price for {symbol} in {months} month(s): ${predicted_price:.2f}")

# Suggested buying point
buying_point = train_and_predict(data.values, window_size, days_in_month) * 0.95  # 5% below the 1-month prediction
print(f"Suggested buying point within 1 month: ${buying_point:.2f}")

# Potential peak 
predicted_prices = [train_and_predict(data.values, window_size, days_in_month * m) for m in forecast_months]
highest_predicted_price = max(predicted_prices)
print(f"Highest predicted price for {symbol} in the next 3 months: ${highest_predicted_price:.2f}")
