import pandas as pd
import configparser
from data_fetching import fetch_data, load_api_keys, load_trade_values, initialize_binance
from forecasting.perform_forecasts import perform_forecasts_model_1, perform_forecasts_model_2
from trading_strategies.dynamic_trading_strategy import dynamic_trading_strategy
from performance import calculate_mape, print_mape, backtest

# Config dosyasını yükle
config = configparser.ConfigParser()
config.read('config.ini')

# Config'den değerleri al
api_key_path = config['DEFAULT']['api_key_path']
trade_values_path = config['DEFAULT']['trade_values_path']

# API anahtarlarını yükle
api_key, api_secret = load_api_keys(api_key_path)
client = initialize_binance(api_key, api_secret)

# İşlem değerlerini yükle
trade_values = load_trade_values(trade_values_path)
symbol = trade_values['symbol']
timeframe = trade_values['timeframe']
start_date = trade_values['start_date']
end_date = trade_values['end_date']
forecast_steps = int(trade_values['forecast_steps'])
initial_balance = float(trade_values['balance'])
use_model_1 = trade_values['use_model_1'].lower() == 'true'
use_model_2 = trade_values['use_model_2'].lower() == 'true'

print(f"Using symbol: {symbol}")

# Veriyi çek
data = fetch_data(client, symbol, timeframe, start_date, end_date)
df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
df.set_index('timestamp', inplace=True)

# Teknik göstergeler ekle
df['rsi'] = df['close'].rolling(window=14).apply(lambda x: (x.diff().mean() / x.abs().mean()) * 100)

# Model 1 veya Model 2'yi kullanarak tahmin yap
forecasts = None
if use_model_1:
    forecasts = perform_forecasts_model_1(df, forecast_steps)
    print(f"Model-1 Forecasts: {forecasts}")
elif use_model_2:
    forecasts = perform_forecasts_model_2(df, forecast_steps)
    print(f"Model-2 Forecasts: {forecasts}")

# Tahminlerin None olmadığından emin olun
if forecasts is None:
    raise ValueError("Tahminler NoneType, lütfen tahmin fonksiyonlarını kontrol edin.")

# Dinamik işlem stratejisini uygulayın
df = dynamic_trading_strategy(df, forecasts)

# Backtest
backtest_results = backtest(df, forecasts, initial_balance)

# MAPE hesapla ve yazdır
mapes = calculate_mape(df, forecasts, start_date, forecast_steps)
print_mape(mapes)

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
