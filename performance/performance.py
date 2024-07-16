import numpy as np

def calculate_mape(actual, forecast):
    actual, forecast = np.array(actual), np.array(forecast)
    if len(actual) == 0:
        raise ValueError("No actual values found for the specified start_date and steps.")
    return np.mean(np.abs((actual - forecast) / actual)) * 100

def print_mape(mape):
    print(f'Mean Absolute Percentage Error (MAPE): {mape:.2f}%')
