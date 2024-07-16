# data_fetching/initialize_binance.py

import ccxt

def initialize_binance(api_key, api_secret):
    exchange = ccxt.binance({
        'apiKey': api_key,
        'secret': api_secret,
        'options': {
            'defaultType': 'future'
        }
    })
    return exchange
