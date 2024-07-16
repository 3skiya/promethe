import configparser
import pandas as pd
import tensorflow as tf
from binance.client import Client
from data_fetching.data_fetching import fetch_data, load_api_keys, load_trade_values, initialize_binance
from trading_strategies.dynamic_trading_strategy import dynamic_trading_strategy
from performance import calculate_mape, print_mape, backtest

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
use_model_1 = trade_values.getboolean('use_model_1', fallback=False)
use_model_2 = trade_values.getboolean('use_model_2', fallback=False)
use_model_3 = trade_values.getboolean('use_model_3', fallback=False)
use_model_4 = trade_values.getboolean('use_model_4', fallback=False)
use_model_5 = trade_values.getboolean('use_model_5', fallback=False)
use_model_6 = trade_values.getboolean('use_model_6', fallback=False)
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
if use_model_1:
    from forecasting.perform_forecasts import perform_forecasts_model_1
    forecasts = perform_forecasts_model_1(df, forecast_steps)
    print(f"Model-1 Forecasts: {forecasts}")
elif use_model_2:
    from forecasting.perform_forecasts import perform_forecasts_model_2
    forecasts = perform_forecasts_model_2(df, forecast_steps)
    print(f"Model-2 Forecasts: {forecasts}")
elif use_model_3:
    from forecasting.perform_forecasts import perform_forecasts_model_3
    forecasts = perform_forecasts_model_3(df, forecast_steps)
    print(f"Model-3 Forecasts: {forecasts}")
elif use_model_4:
    from forecasting.perform_forecasts import perform_forecasts_model_4
    forecasts = perform_forecasts_model_4(df, forecast_steps)
    print(f"Model-4 Forecasts: {forecasts}")
elif use_model_5:
    from forecasting.perform_forecasts import perform_forecasts_model_5
    forecasts = perform_forecasts_model_5(df, forecast_steps)
    print(f"Model-5 Forecasts: {forecasts}")
elif use_model_6:
    from forecasting.perform_forecasts import perform_forecasts_model_6
    forecasts = perform_forecasts_model_6(df, forecast_steps)
    print(f"Model-6 Forecasts: {forecasts}")
else:
    raise ValueError("No model selected in configuration.")

if forecasts is None:
    raise ValueError("Tahminler NoneType, lütfen tahmin fonksiyonlarını kontrol edin.")

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
    'Forecast': forecasts,
    'Actual': actual_prices
})

# Fark ve yüzde fark hesaplama
forecast_df['Difference'] = forecast_df['Actual'] - forecast_df['Forecast']
forecast_df['Percentage Difference (%)'] = (forecast_df['Difference'] / forecast_df['Actual']) * 100

# Apply trading strategy
df = dynamic_trading_strategy(df, forecasts)

# Perform backtest
backtest_results = backtest(df, forecasts, initial_balance)
print(backtest_results)

# Summary of forecasts and backtest results
print("\nForecast Summary:")
for i, row in forecast_df.iterrows():
    print(f"Date: {row['Date']}, Forecast: {int(row['Forecast']):,}, Actual: {int(row['Actual']):,}, Difference: {int(row['Difference']):,}, Percentage Difference (%): {row['Percentage Difference (%)']:.2f}%")

print("\nBacktest Summary:")
print(f"Initial Balance: {int(backtest_results['initial_balance']):,}")
print(f"Profit: {int(backtest_results['profit']):,}")
print(f"Number of Trades: {backtest_results['trades']}")
