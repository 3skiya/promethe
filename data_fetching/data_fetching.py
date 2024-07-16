from binance.client import Client
import pandas as pd
import configparser

def load_api_keys(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        api_key = lines[0].strip().split('=')[1]
        api_secret = lines[1].strip().split('=')[1]
    return api_key, api_secret

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
            kline[6],  # close time
            kline[7],  # quote asset volume
            kline[8],  # number of trades
            kline[9],  # taker buy base asset volume
            kline[10], # taker buy quote asset volume
            kline[11]  # ignore
        ])
    return data

def load_trade_values(file_path):
    config = configparser.ConfigParser()
    with open(file_path, 'r') as f:
        config.read_file(f)
    if not config.sections() and 'DEFAULT' not in config:
        raise ValueError(f"Config file {file_path} is empty or not formatted correctly.")
    trade_values = {}
    for key in config['DEFAULT']:
        trade_values[key] = config['DEFAULT'][key]
    return trade_values

def initialize_binance(api_key, api_secret):
    client = Client(api_key, api_secret)
    return client
