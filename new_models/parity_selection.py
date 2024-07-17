# parity_selection.py

import ccxt
import pandas as pd
import numpy as np
import pandas_ta as ta
from config import load_config

def fetch_ohlcv(symbol, timeframe, exchange, since=None):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since=since)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

def analyze_technical_indicators(df, config):
    if config['use_rsi']:
        df['rsi'] = ta.rsi(df['close'], length=14)
    if config['use_macd']:
        macd = ta.macd(df['close'])
        df['macd'] = macd['MACD_12_26_9']
        df['macd_signal'] = macd['MACDs_12_26_9']
        df['macd_hist'] = macd['MACDh_12_26_9']
    if config['use_stochastic']:
        stoch = ta.stoch(df['high'], df['low'], df['close'])
        df['stoch_k'] = stoch['STOCHk_14_3_3'].astype(float)
        df['stoch_d'] = stoch['STOCHd_14_3_3'].astype(float)
    if config['use_bollinger_bands']:
        bollinger = ta.bbands(df['close'])
        df['bollinger_upper'] = bollinger['BBU_5_2.0'].astype(float)
        df['bollinger_middle'] = bollinger['BBM_5_2.0'].astype(float)
        df['bollinger_lower'] = bollinger['BBL_5_2.0'].astype(float)
    return df

def evaluate_parity(df, config):
    score = 0
    if config['use_rsi']:
        rsi_overbought = df['rsi'] > 70
        rsi_oversold = df['rsi'] < 30
        if rsi_oversold.any():
            score += 1
        if rsi_overbought.any():
            score -= 1
    if config['use_macd']:
        macd_bullish = df['macd'] > df['macd_signal']
        macd_bearish = df['macd'] < df['macd_signal']
        if macd_bullish.any():
            score += 1
        if macd_bearish.any():
            score -= 1
    if config['use_stochastic']:
        stoch_overbought = df['stoch_k'] > 80
        stoch_oversold = df['stoch_k'] < 20
        if stoch_oversold.any():
            score += 1
        if stoch_overbought.any():
            score -= 1
    if config['use_bollinger_bands']:
        price_above_bollinger_upper = df['close'] > df['bollinger_upper']
        price_below_bollinger_lower = df['close'] < df['bollinger_lower']
        if price_below_bollinger_lower.any():
            score += 1
        if price_above_bollinger_upper.any():
            score -= 1
    
    return score

def select_best_parity(symbols, timeframe, exchange, config):
    best_score = -np.inf
    best_symbol = None
    for symbol in symbols:
        df = fetch_ohlcv(symbol, timeframe, exchange)
        df = analyze_technical_indicators(df, config)
        score = evaluate_parity(df, config)
        print(f"Symbol: {symbol}, Score: {score}")
        if score > best_score:
            best_score = score
            best_symbol = symbol
    return best_symbol

def update_trade_values(best_symbol):
    with open('TradeValues.txt', 'w') as file:
        file.write(f"symbol={best_symbol}\n")
        file.write("timeframe=4h\n")
        file.write("balance=1000\n")
        file.write("budget=100\n")
        file.write("leverage=10\n")
        file.write("hedge=false\n")
        file.write("start_date=2023-01-01T00:00:00Z\n")
        file.write("end_date=2024-01-01T00:00:00Z\n")
        file.write("backtest_start_date=2023-06-09\n")

if __name__ == "__main__":
    exchange = ccxt.binance()
    symbols = ['BTC/USDT', 'ETH/USDT', 'XRP/USDT', 'LTC/USDT', 'BCH/USDT']
    timeframe = '4h'
    config = load_config('config.txt')
    best_symbol = select_best_parity(symbols, timeframe, exchange, config)
    print(f"Selected Best Symbol: {best_symbol}")
    update_trade_values(best_symbol)
