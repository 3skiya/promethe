import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
from binance.client import Client
import configparser
import os
import numpy as np

# Binance API anahtarlarını yükle
config = configparser.ConfigParser()
config.read('api.txt')
api_key = config['DEFAULT']['api_key']
api_secret = config['DEFAULT']['api_secret']

# Binance API'ye bağlan
client = Client(api_key, api_secret)

# TradeValues.txt dosyasını okuyup yükle
trade_values = configparser.ConfigParser()
trade_values.read('TradeValues.txt')
symbol = trade_values['DEFAULT']['symbol']
timeframe = trade_values['DEFAULT']['timeframe']
start_date = trade_values['DEFAULT']['start_date']
end_date = trade_values['DEFAULT']['end_date']

# Veri çekme
klines = client.get_historical_klines(symbol, timeframe, start_date, end_date)
data = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])

# DataFrame'i uygun formatta kaydetme
os.makedirs('linear_regression_data', exist_ok=True)
file_path = f'linear_regression_data/{symbol}_LinearRegression_data.csv'
data.to_csv(file_path, index=False)

# Veri yükleme ve ön işleme
df = pd.read_csv(file_path)
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(df['close'].values.reshape(-1, 1))

# Model oluşturma
X_train = np.arange(len(scaled_data)).reshape(-1, 1)
y_train = scaled_data

model = LinearRegression()
model.fit(X_train, y_train)

# Modeli kaydetme
os.makedirs('new_models', exist_ok=True)
with open('new_models/linear_regression_model.pkl', 'wb') as file:
    import pickle
    pickle.dump(model, file)
