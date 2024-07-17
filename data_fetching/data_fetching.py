import configparser
from binance.client import Client
import pandas as pd

def load_api_keys(filepath):
    config = configparser.ConfigParser()
    config.read(filepath)
    return config['DEFAULT']['api_key'], config['DEFAULT']['api_secret']

def initialize_binance(api_key, api_secret):
    return Client(api_key, api_secret)

def fetch_data(client, symbol, timeframe, start_date, end_date):
    klines = client.get_historical_klines(symbol, timeframe, start_date, end_date)
    data = []
    for kline in klines:
        data.append([
            kline[0],  # timestamp
            kline[1],  # open
            kline[2],  # high
            kline[3],  # low
            kline[4],  # close
            kline[5],  # volume
            kline[6],  # close_time
            kline[7],  # quote_asset_volume
            kline[8],  # number_of_trades
            kline[9],  # taker_buy_base_asset_volume
            kline[10], # taker_buy_quote_asset_volume
            kline[11]  # ignore
        ])
    df = pd.DataFrame(data, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
    ])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    
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
    
    return df
