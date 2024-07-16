# data_fetching/load_trade_values.py

def load_trade_values(filepath):
    trade_values = {}
    with open(filepath, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            trade_values[key] = value
    return trade_values
