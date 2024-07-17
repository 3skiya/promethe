import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Input, LeakyReLU
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
os.makedirs('gan_data', exist_ok=True)
file_path = f'gan_data/{symbol}_GAN_data.csv'
data.to_csv(file_path, index=False)

# Veri yükleme ve ön işleme
df = pd.read_csv(file_path)
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(df['close'].values.reshape(-1, 1))

# GAN modeli oluşturma
def create_generator():
    generator = Sequential()
    generator.add(Dense(128, input_dim=100))
    generator.add(LeakyReLU(alpha=0.01))
    generator.add(Dense(1, activation='linear'))
    return generator

def create_discriminator():
    discriminator = Sequential()
    discriminator.add(Dense(128, input_dim=1))
    discriminator.add(LeakyReLU(alpha=0.01))
    discriminator.add(Dense(1, activation='sigmoid'))
    return discriminator

def create_gan(discriminator, generator):
    discriminator.trainable = False
    gan_input = Input(shape=(100,))
    x = generator(gan_input)
    gan_output = discriminator(x)
    gan = Model(gan_input, gan_output)
    gan.compile(loss='binary_crossentropy', optimizer='adam')
    return gan

generator = create_generator()
discriminator = create_discriminator()
discriminator.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
gan = create_gan(discriminator, generator)

# GAN modeli eğitimi
epochs = 10000
batch_size = 32

for epoch in range(epochs):
    idx = np.random.randint(0, scaled_data.shape[0], batch_size)
    real_data = scaled_data[idx]
    noise = np.random.normal(0, 1, (batch_size, 100))
    generated_data = generator.predict(noise)
    
    d_loss_real = discriminator.train_on_batch(real_data, np.ones((batch_size, 1)))
    d_loss_fake = discriminator.train_on_batch(generated_data, np.zeros((batch_size, 1)))
    d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)
    
    noise = np.random.normal(0, 1, (batch_size, 100))
    valid_y = np.array([1] * batch_size)
    g_loss = gan.train_on_batch(noise, valid_y)
    
    if epoch % 1000 == 0:
        print(f"{epoch} [D loss: {d_loss[0]}, acc.: {100*d_loss[1]}%] [G loss: {g_loss}]")
        # Modelleri kontrol noktalarında kaydet
        generator.save(f'new_models/gan_generator_epoch_{epoch}.h5')
        discriminator.save(f'new_models/gan_discriminator_epoch_{epoch}.h5')

# Nihai modelleri kaydetme
os.makedirs('new_models', exist_ok=True)
generator.save('new_models/gan_generator.h5')
discriminator.save('new_models/gan_discriminator.h5')
