import pandas as pd
import numpy as np

def dynamic_trading_strategy(df, forecasts):
    df['rsi'] = calculate_rsi(df['close'])
    df['signal'] = 'hold'
    for i in range(len(df) - len(forecasts), len(df)):
        rsi = df.loc[i, 'rsi']
        if rsi < 30 and forecasts[i - (len(df) - len(forecasts))] > df.loc[i, 'close']:
            df.loc[i, 'signal'] = 'buy'
        elif rsi > 70 and forecasts[i - (len(df) - len(forecasts))] < df.loc[i, 'close']:
            df.loc[i, 'signal'] = 'sell'
    return df

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - 100 / (1 + rs)
