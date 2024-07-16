# trading_strategies/add_technical_indicators.py

import pandas_ta as ta

def add_technical_indicators(df):
    df['rsi'] = ta.rsi(df['close'], length=14)
    macd = ta.macd(df['close'])
    df['macd'] = macd['MACD_12_26_9']
    df['macd_signal'] = macd['MACDs_12_26_9']
    df['macd_hist'] = macd['MACDh_12_26_9']
    stoch = ta.stoch(df['high'], df['low'], df['close'])
    df['stoch_k'] = stoch['STOCHk_14_3_3']
    df['stoch_d'] = stoch['STOCHd_14_3_3']
    bollinger = ta.bbands(df['close'])
    df['bollinger_upper'] = bollinger['BBU_5_2.0']
    df['bollinger_middle'] = bollinger['BBM_5_2.0']
    df['bollinger_lower'] = bollinger['BBL_5_2.0']
    return df
