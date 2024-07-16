import numpy as np

def calculate_mape(df, forecasts, start_date, steps):
    actual = df.loc[start_date:].iloc[:steps]['close']
    mape_arima = np.mean(np.abs((actual - forecasts['arima']) / actual)) * 100
    mape_prophet = np.mean(np.abs((actual - forecasts['prophet']) / actual)) * 100
    mape_lstm = np.mean(np.abs((actual - forecasts['lstm']) / actual)) * 100
    return {
        'arima': mape_arima,
        'prophet': mape_prophet,
        'lstm': mape_lstm
    }

def print_mape(mapes):
    print(f"ARIMA MAPE: {mapes['arima']:.2f}%")
    print(f"Prophet MAPE: {mapes['prophet']:.2f}%")
    print(f"LSTM MAPE: {mapes['lstm']:.2f}%")
