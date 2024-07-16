import pandas as pd
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import numpy as np

def perform_forecasts(df, forecast_steps, start_date, use_arima, use_prophet, use_lstm):
    forecasts = {}

    # CNN, LSTM, GRU modelleri burada tanımlanacak
    # Örneğin: LSTM Modeli
    if use_lstm:
        model = load_model('new_models/lstm_model.h5')
        data = df['close'].values.reshape(-1, 1)
        scaler = MinMaxScaler()
        scaled_data = scaler.fit_transform(data)
        X_test = []
        for i in range(60, len(scaled_data)):
            X_test.append(scaled_data[i-60:i, 0])
        X_test = np.array(X_test)
        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
        predictions = model.predict(X_test)
        predictions = scaler.inverse_transform(predictions)
        forecasts['lstm'] = predictions.flatten()[-forecast_steps:].tolist()

    return forecasts
