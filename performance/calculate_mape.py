import numpy as np
import pandas as pd

def calculate_mape(df, forecasts, start_date, steps):
    actual = df[df['timestamp'] >= pd.to_datetime(start_date)]['close'][:steps]
    
    if len(actual) == 0:
        print(f"DataFrame start date: {df['timestamp'].min()}, end date: {df['timestamp'].max()}")
        print(f"Requested start date: {start_date}, steps: {steps}")
        raise ValueError("No actual values found for the specified start_date and steps.")
    
    mape_arima = np.mean(np.abs((actual - forecasts['arima']) / actual)) * 100 if 'arima' in forecasts else None
    mape_prophet = np.mean(np.abs((actual - forecasts['prophet']) / actual)) * 100 if 'prophet' in forecasts else None
    mape_lstm = np.mean(np.abs((actual - forecasts['lstm']) / actual)) * 100 if 'lstm' in forecasts else None

    return {'arima': mape_arima, 'prophet': mape_prophet, 'lstm': mape_lstm}
