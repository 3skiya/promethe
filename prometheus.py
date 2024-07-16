import pandas as pd
import numpy as np
import configparser  # configparser modülünü içe aktardık
from data_fetching import fetch_data, load_api_keys, load_trade_values, initialize_binance
from trading_strategies.dynamic_trading_strategy import dynamic_trading_strategy
from performance import calculate_mape, print_mape, plot_forecasts
from forecasting.perform_forecasts import perform_forecasts_model_1, perform_forecasts_model_2
from backtesting.backtesting import backtest

# API ve konfigürasyon dosyalarını yükle
api_key_path = 'api.txt'
trade_values_path = 'TradeValues.txt'

# API anahtarlarını yükle
api_key, api_secret = load_api_keys(api_key_path)

# Binance API'yi başlat
client = initialize_binance(api_key, api_secret)

# Trade değerlerini yükle
trade_values = load_trade_values(trade_values_path)

# Konfigürasyon değerlerini al
symbol = trade_values['symbol']
timeframe = trade_values['timeframe']
start_date = trade_values['start_date']
end_date = trade_values['end_date']
forecast_steps = int(trade_values['forecast_steps'])
initial_balance = float(trade_values['balance'])
use_model_1 = trade_values['use_model_1'].lower() == 'true'
use_model_2 = trade_values['use_model_2'].lower() == 'true'

print(f"Using symbol: {symbol}")

# Verileri çek
data = fetch_data(client, symbol.replace("/", ""), timeframe, start_date, end_date)
print("Fetched data:", data)  # Veriyi ekrana yazdır

# DataFrame'e dönüştür
df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

# Zaman damgasını tarihe çevir
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
df.set_index('timestamp', inplace=True)

# Model tahminlerini gerçekleştir
if use_model_1:
    forecasts = perform_forecasts_model_1(df, forecast_steps)
    model_used = "Model-1 (ARIMA, Prophet, LSTM)"
elif use_model_2:
    forecasts = perform_forecasts_model_2(df, forecast_steps)
    model_used = "Model-2 (LSTM from GitHub)"
else:
    forecasts = None

print(f"{model_used} Forecasts:", forecasts)

if forecasts is None:
    raise ValueError("Tahminler NoneType, lütfen tahmin fonksiyonlarını kontrol edin.")

# Dinamik ticaret stratejisini uygula
df = dynamic_trading_strategy(df, forecasts)

# Backtest'i başlat
backtest_results = backtest(df, forecasts, initial_balance)

# Backtest sonuçlarını yazdır
print("Backtest results:", backtest_results)

# Sonuçları özetle
plot_forecasts(df, forecasts, backtest_results)

print(f"Kullanılan Model: {model_used}")

# Günlük sonuçları yazdır
for i in range(len(df)):
    print("--------------------------------------------------")
    print(f"{df.index[i].date()}")
    rsi = df.loc[df.index[i], 'rsi'] if 'rsi' in df.columns else "Hesaplanmadı"
    print(f"RSI: {rsi}")
    print(f"Price: ${df.loc[df.index[i], 'close']:.2f}")
    forecast_price = forecasts[i] if i < len(forecasts) else "N/A"
    print(f"Forecast: ${forecast_price:.2f}")
    signal = df.loc[df.index[i], 'signal'] if 'signal' in df.columns else "No Trade"
    print(f"Result: {signal}")
    print(f"Total Trades: {backtest_results['Total Trades']}, Wins: {backtest_results['Wins']}, Losses: {backtest_results['Losses']}, Final Balance: ${backtest_results['Final Balance']:.2f}, Max Drawdown: {backtest_results['Max Drawdown']:.2f}%, Total ROI: {backtest_results['Total ROI']:.2f}%, Total PNL: ${backtest_results['Total PNL']:.2f}")
    print("--------------------------------------------------")
