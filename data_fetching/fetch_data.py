import ccxt
import pandas as pd

def fetch_data(symbol, timeframe, exchange, since=None, until=None):
    since_timestamp = exchange.parse8601(since) if since else None
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since=since_timestamp, limit=None)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    if until:
        until_timestamp = pd.to_datetime(until)
        until_timestamp = pd.Timestamp(until_timestamp).tz_localize(None)  # Make sure both are timezone naive
        df['timestamp'] = df['timestamp'].dt.tz_localize(None)
        df = df[df['timestamp'] <= until_timestamp]
    return df
