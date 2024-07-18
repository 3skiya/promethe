import configparser
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import os
import sys

# `data_fetching` modülünü import edebilmek için sys.path'e dizin ekleme
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'data_fetching'))
from data_fetching import fetch_data, load_api_keys, initialize_binance

# Load configuration
config_path = os.path.join(os.path.dirname(__file__), '..', 'TradeValues.txt')
config = configparser.ConfigParser()
config.read(config_path)

# Extract values from configuration
trade_values = config['DEFAULT']
symbol = trade_values['symbol'].replace("/", "")
timeframe = trade_values['timeframe']
start_date = trade_values['start_date']
end_date = trade_values['end_date']

# Binance API keys
api_key_path = os.path.join(os.path.dirname(__file__), '..', 'api.txt')
api_key, api_secret = load_api_keys(api_key_path)
client = initialize_binance(api_key, api_secret)

# Fetch data
df = fetch_data(client, symbol, timeframe, start_date, end_date)
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
df.set_index('timestamp', inplace=True)
df['close'] = pd.to_numeric(df['close'])

# ARIMA model training
print("Starting ARIMA model training...")
model = ARIMA(df['close'], order=(5, 1, 0))
model_fit = model.fit()
print(model_fit.summary())

# Create directory if not exists
output_dir = os.path.join(os.path.dirname(__file__), 'models')
os.makedirs(output_dir, exist_ok=True)

# Save the model
model_fit.save(os.path.join(output_dir, 'arima_model.pkl'))
print("ARIMA model training complete.")
