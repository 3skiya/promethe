import configparser
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from data_fetching.data_fetching import fetch_data, load_api_keys, initialize_binance

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

# Binance API keys
api_key_path = 'api.txt'
api_key, api_secret = load_api_keys(api_key_path)
client = initialize_binance(api_key, api_secret)

# Fetch data
data = fetch_data(client, symbol, timeframe, start_date, end_date)
df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
df.set_index('timestamp', inplace=True)

# ARIMA model training
model = ARIMA(df['close'], order=(5, 1, 0))
model_fit = model.fit()

# Save the model
model_fit.save('new_models/arima_model.pkl')
print("ARIMA model training complete.")
