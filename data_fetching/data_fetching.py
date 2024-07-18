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
    return df
