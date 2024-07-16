import pandas as pd

def dynamic_trading_strategy(df, forecasts):
    df['signal'] = 'hold'
    for i in range(len(df) - len(forecasts), len(df)):
        if pd.isnull(df.loc[i, 'rsi']):
            rsi = 'Hesaplanmadı'
        else:
            rsi = df.loc[i, 'rsi']
        
        if rsi < 30 and forecasts[i - (len(df) - len(forecasts))] > df.loc[i, 'close']:
            df.loc[i, 'signal'] = 'buy'
        elif rsi > 70 and forecasts[i - (len(df) - len(forecasts))] < df.loc[i, 'close']:
            df.loc[i, 'signal'] = 'sell'
    
    return df

def add_technical_indicators(df):
    # RSI hesaplamasını ekleyin
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))
    
    # Diğer teknik indikatörler eklenebilir
    return df
