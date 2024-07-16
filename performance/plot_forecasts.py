import matplotlib.pyplot as plt
import pandas as pd

def plot_forecasts(df, forecasts, start_date, forecast_steps, plot_graphs):
    if plot_graphs:
        plt.figure(figsize=(8, 6))  # 800x600 piksel
        plt.plot(df['timestamp'], df['close'], label='Actual Price')
        
        forecast_dates = df['timestamp'][-forecast_steps:]
        
        if 'arima' in forecasts:
            plt.plot(forecast_dates, forecasts['arima'], label='ARIMA Forecast')
        if 'prophet' in forecasts:
            plt.plot(forecast_dates, forecasts['prophet'], label='Prophet Forecast')
        if 'lstm' in forecasts:
            plt.plot(forecast_dates, forecasts['lstm'], label='LSTM Forecast')
        
        plt.axvline(pd.to_datetime(start_date), color='r', linestyle='--', label='Forecast Start')
        plt.legend()
        plt.show()
