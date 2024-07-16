# live_simulation/live_trading_simulation.py

import time
import pandas as pd
from datetime import datetime, timedelta
from trading_strategies.add_technical_indicators import add_technical_indicators
from trading_strategies.dynamic_trading_strategy import dynamic_trading_strategy
from forecasting.perform_forecasts import perform_forecasts

def fetch_live_data(symbol, timeframe, exchange, limit=100):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

def live_trading_simulation(exchange, trade_values, use_arima, use_prophet, use_lstm):
    symbol = trade_values.get('symbol')
    timeframe = trade_values.get('timeframe')
    balance = float(trade_values.get('balance', 1000))
    budget = float(trade_values.get('budget', 100))
    leverage = int(trade_values.get('leverage', 10))
    hedge = trade_values.get('hedge', 'false').lower() in ['true', '1', 'yes']
    
    iteration = 0
    max_iterations = 60  # Example: Run for 60 iterations
    while iteration < max_iterations:
        print(f"Iteration {iteration + 1}/{max_iterations}")
        try:
            print("Fetching live data...")
            df = fetch_live_data(symbol, timeframe, exchange)
            print("Live data fetched.")
            
            forecast_steps = 10
            forecasts = perform_forecasts(df, forecast_steps, None, use_arima, use_prophet, use_lstm)
            
            print(f"Forecasts: {forecasts}")
            
            df = add_technical_indicators(df)
            df = dynamic_trading_strategy(df, forecasts)
            print("Trading signals generated.")
            
            signal = df['signal'].iloc[-1]
            last_close = df['close'].iloc[-1]
            print(f"Fetched live data: {df.iloc[-1].to_dict()}")
            print(f"Last signal: {signal}")
            
            # Perform trading action based on the signal
            if signal == 'buy':
                print("Executing buy order...")
                # Simulate buy order logic here
            elif signal == 'sell':
                print("Executing sell order...")
                # Simulate sell order logic here
            
            print(f"Current balance: {balance} USD")
            
            # Wait before the next iteration
            time.sleep(10)  # Example: Wait 10 seconds
            iteration += 1
        except Exception as e:
            print(f"Error during live trading iteration {iteration + 1}: {e}")
            break
