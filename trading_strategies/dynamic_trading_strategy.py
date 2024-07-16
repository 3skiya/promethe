import numpy as np
import pandas as pd

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period, min_periods=1).mean()
    avg_loss = loss.rolling(window=period, min_periods=1).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def dynamic_trading_strategy(df, forecasts):
    df['rsi'] = calculate_rsi(df['close'])
    
    for i in range(1, len(df)):
        rsi = df.iloc[i]['rsi']
        if rsi < 30:
            df.loc[df.index[i], 'signal'] = 'buy'
        elif rsi > 70:
            df.loc[df.index[i], 'signal'] = 'sell'
        else:
            df.loc[df.index[i], 'signal'] = 'hold'
    
    return df
#v.1.1
