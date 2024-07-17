import configparser
import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense
from sklearn.preprocessing import MinMaxScaler
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

# Verileri sayısal türe dönüştürme
df['close'] = pd.to_numeric(df['close'])

# Hareketli Ortalama (Moving Average) ekleme
df['SMA_20'] = df['close'].rolling(window=20).mean()
df['SMA_50'] = df['close'].rolling(window=50).mean()

# RSI (Relative Strength Index) ekleme
delta = df['close'].diff(1)
gain = delta.where(delta > 0, 0)
loss = -delta.where(delta < 0, 0)
avg_gain = gain.rolling(window=14).mean()
avg_loss = loss.rolling(window=14).mean()
rs = avg_gain / avg_loss
df['RSI'] = 100 - (100 / (1 + rs))

# Preprocess data
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(df[['close', 'SMA_20', 'SMA_50', 'RSI']].dropna())

# Prepare training data
prediction_days = 60
x_train, y_train = [], []
for x in range(prediction_days, len(scaled_data)):
    x_train.append(scaled_data[x-prediction_days:x])
    y_train.append(scaled_data[x, 0])
x_train, y_train = np.array(x_train), np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], x_train.shape[2]))

# CNN model training
print("Starting CNN model training...")
model = Sequential()
model.add(Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=(x_train.shape[1], x_train.shape[2])))
model.add(MaxPooling1D(pool_size=2))
model.add(Flatten())
model.add(Dense(50, activation='relu'))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mean_squared_error')
history = model.fit(x_train, y_train, epochs=25, batch_size=32, verbose=1)

# Training history
print("CNN model training history:")
print(history.history)

# Create directory if not exists
output_dir = os.path.join(os.path.dirname(__file__), 'models')
os.makedirs(output_dir, exist_ok=True)

# Save the model
model.save(os.path.join(output_dir, 'cnn_model.h5'))
print("CNN model training complete.")
