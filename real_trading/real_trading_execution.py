# real_trading/real_trading_execution.py

from trading_strategies.add_technical_indicators import add_technical_indicators
from trading_strategies.dynamic_trading_strategy import dynamic_trading_strategy
from forecasting.perform_forecasts import perform_forecasts
import pandas as pd

def fetch_live_data(symbol, timeframe, exchange, limit=100):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

def place_order(exchange, symbol, order_type, amount, price=None):
    try:
        if order_type == 'buy':
            order = exchange.create_market_buy_order(symbol, amount)
        elif order_type == 'sell':
            order = exchange.create_market_sell_order(symbol, amount)
        else:
            raise ValueError("Invalid order type. Use 'buy' or 'sell'.")
        return order
    except Exception as e:
        print(f"Error placing order: {e}")
        return None

def real_trading_execution(exchange, trade_values):
    symbol = trade_values.get('symbol')
    timeframe = trade_values.get('timeframe')
    balance = float(trade_values.get('balance', 1000))
    budget = float(trade_values.get('budget', 100))
    leverage = int(trade_values.get('leverage', 10))
    hedge = trade_values.get('hedge', 'false').lower() in ['true', '1', 'yes']
    
    print(f"Starting real trading execution for {symbol}...")
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
        
        amount = budget / last_close
        
        # Perform trading action based on the signal
        if signal == 'buy':
            print("Placing buy order...")
            order = place_order(exchange, symbol, 'buy', amount)
        elif signal == 'sell':
            print("Placing sell order...")
            order = place_order(exchange, symbol, 'sell', amount)
        
        print(f"Current balance: {balance} USD")
    except Exception as e:
        print(f"Error during real trading execution: {e}")
