import configparser
import pandas as pd
import tensorflow as tf
from binance.client import Client
from data_fetching.data_fetching import fetch_data, load_api_keys, load_trade_values, initialize_binance
from trading_strategies.dynamic_trading_strategy import dynamic_trading_strategy
from performance import calculate_mape, print_mape, backtest
from Prediction import predict

# Load configuration
config_path = 'TradeValues.txt'
config = configparser.ConfigParser()
config.read(config_path)

# Extract values from configuration
trade_values = config['DEFAULT']
symbol = trade_values['symbol'].replace("/", "")
timeframe = trade_values['timeframe']
start_date = trade_values['start_date']
end_date = trade_values['end_date']
forecast_steps = int(trade_values['forecast_steps'])
use_arima = trade_values.getboolean('use_arima', fallback=False)
use_lstm = trade_values.getboolean('use_lstm', fallback=False)
use_cnn = trade_values.getboolean('use_cnn', fallback=False)
use_gru = trade_values.getboolean('use_gru', fallback=False)
use_gru_wf = trade_values.getboolean('use_gru_wf', fallback=False)
use_linear_regression = trade_values.getboolean('use_linear_regression', fallback=False)
use_gan = trade_values.getboolean('use_gan', fallback=False)
use_prediction = trade_values.getboolean('use_prediction', fallback=False)
initial_balance = float(trade_values['balance'])

# Binance API keys
api_key_path = 'api.txt'
api_key, api_secret = load_api_keys(api_key_path)
client = initialize_binance(api_key, api_secret)

# Fetch data
print(f"Using symbol: {symbol}")
data = fetch_data(client, symbol, timeframe, start_date, end_date)

# Ensure the 'timestamp' column exists
columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore']
df = pd.DataFrame(data, columns=columns)

# Convert 'timestamp' to datetime and set as index
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
df.set_index('timestamp', inplace=True)
df = df[['open', 'high', 'low', 'close', 'volume']]

# Convert columns to numeric values
df[['open', 'high', 'low', 'close', 'volume']] = df[['open', 'high', 'low', 'close', 'volume']].apply(pd.to_numeric)

# Perform forecasts
forecasts = {}
if use_arima:
    from forecasting.perform_forecasts import perform_forecasts_model_1
    forecasts['ARIMA'] = perform_forecasts_model_1(df, forecast_steps)
    print(f"ARIMA Forecasts: {forecasts['ARIMA']}")
if use_lstm:
    from forecasting.perform_forecasts import perform_forecasts_model_2
    forecasts['LSTM'] = perform_forecasts_model_2(df, forecast_steps)
    print(f"LSTM Forecasts: {forecasts['LSTM']}")
if use_cnn:
    from forecasting.perform_forecasts import perform_forecasts_model_3
    forecasts['CNN'] = perform_forecasts_model_3(df, forecast_steps)
    print(f"CNN Forecasts: {forecasts['CNN']}")
if use_gru:
    from forecasting.perform_forecasts import perform_forecasts_model_4
    forecasts['GRU'] = perform_forecasts_model_4(df, forecast_steps)
    print(f"GRU Forecasts: {forecasts['GRU']}")
if use_gru_wf:
    from forecasting.perform_forecasts import perform_forecasts_model_5
    forecasts['GRU_WF'] = perform_forecasts_model_5(df, forecast_steps)
    print(f"GRU_WF Forecasts: {forecasts['GRU_WF']}")
if use_linear_regression:
    from forecasting.perform_forecasts import perform_forecasts_model_6
    forecasts['Linear Regression'] = perform_forecasts_model_6(df, forecast_steps)
    print(f"Linear Regression Forecasts: {forecasts['Linear Regression']}")
if use_gan:
    from forecasting.perform_forecasts import perform_forecasts_model_7
    forecasts['GAN'] = perform_forecasts_model_7(df, forecast_steps)
    print(f"GAN Forecasts: {forecasts['GAN']}")
if use_prediction:
    predictions = predict(df, 'linear_regression')
    forecasts['Prediction'] = predictions['Prediction'].values[-forecast_steps:]
    print(f"Prediction Forecasts: {forecasts['Prediction']}")

# Gerçek fiyatları Binance API'den çekme
forecast_dates = pd.date_range(start=df.index[-forecast_steps], periods=forecast_steps, freq='H')
actual_prices = []

for date in forecast_dates:
    klines = client.get_historical_klines(symbol, timeframe, str(date), str(date + pd.Timedelta(hours=1)))
    if klines:
        actual_prices.append(float(klines[0][4]))  # 'close' fiyatını al

# Tahmin ve gerçekleşen fiyatları karşılaştırma
forecast_df = pd.DataFrame({
    'Date': forecast_dates,
    'Actual': actual_prices
})

for model_name, model_forecasts in forecasts.items():
    forecast_df[model_name] = model_forecasts

# Apply trading strategy
for model_name, model_forecasts in forecasts.items():
    df = dynamic_trading_strategy(df, model_forecasts)

# Perform backtest
for model_name, model_forecasts in forecasts.items():
    backtest_results = backtest(df, model_forecasts, initial_balance)
    print(f"\nBacktest Summary for {model_name}:")
    print(f"Initial Balance: {int(backtest_results['initial_balance']):,}")
    print(f"Profit: {int(backtest_results['profit']):,}")
    print(f"Number of Trades: {backtest_results['trades']}")

# Summary of forecasts and backtest results
print("\nForecast Summary:")
for i, row in forecast_df.iterrows():
    summary = f"Date: {row['Date']}, Actual: ${int(row['Actual']):,}"
    best_model = None
    best_diff = float('inf')
    for model_name in forecasts.keys():
        forecast_value = row[model_name]
        if pd.isna(forecast_value):
            summary += f", {model_name} Forecast: NaN, Diff: NaN, (%): NaN%"
        else:
            difference = row['Actual'] - forecast_value
            percentage_difference = (difference / row['Actual']) * 100
            summary += f", {model_name} Forecast: ${int(forecast_value):,}, Diff: {int(difference):,}, (%): {percentage_difference:.2f}%"
            if abs(difference) < best_diff:
                best_diff = abs(difference)
                best_model = model_name
    print(summary)
    if best_model:
        print(f"\033[1m\033[94mBest Model for {row['Date']}: {best_model} with Diff: {best_diff:.2f}\033[0m")
