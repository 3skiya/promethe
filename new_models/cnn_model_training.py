import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler
from binance.client import Client
import configparser
import os

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
os.makedirs('cnn_data', exist_ok=True)
file_path = f'cnn_data/{symbol}_CNN_data.csv'
data.to_csv(file_path, index=False)

# Veri yükleme ve ön işleme
df = pd.read_csv(file_path)
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(df['close'].values.reshape(-1, 1))

# Model oluşturma
model = Sequential()
model.add(Conv1D(filters=64, kernel_size=2, activation='relu', input_shape=(60, 1)))
model.add(MaxPooling1D(pool_size=2))
model.add(Flatten())
model.add(Dense(50, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(1))

model.compile(optimizer='adam', loss='mean_squared_error')

# Veri hazırlama
X_train, y_train = [], []
for i in range(60, len(scaled_data)):
    X_train.append(scaled_data[i-60:i, 0])
    y_train.append(scaled_data[i, 0])

X_train, y_train = np.array(X_train), np.array(y_train)
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

# Model eğitimi
model.fit(X_train, y_train, epochs=20, batch_size=32)

# Modeli kaydetme
os.makedirs('new_models', exist_ok=True)
model.save('new_models/cnn_model.h5')
