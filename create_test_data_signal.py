# create_test_data_signal.py
import pandas as pd
from trading_strategies.add_technical_indicators import add_technical_indicators

def create_test_data_signal(df):
    df = add_technical_indicators(df)
    df['signal'] = 'hold'
    df.loc[df['rsi'] < 30, 'signal'] = 'buy'
    df.loc[df['rsi'] > 70, 'signal'] = 'sell'
    return df

if __name__ == "__main__":
    df = pd.read_csv('test_data.csv')
    df = create_test_data_signal(df)
    print(df['signal'].value_counts())
