import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model
import pandas as pd

def perform_forecasts_model_1(df, forecast_steps):
    model = load_model('models/lstm_model.h5')
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(df['close'].values.reshape(-1, 1))
    x_test = []
    for i in range(forecast_steps, len(scaled_data)):
        x_test.append(scaled_data[i-forecast_steps:i, 0])
    x_test = np.array(x_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    predictions = model.predict(x_test)
    predictions = scaler.inverse_transform(predictions)
    return predictions[-forecast_steps:].tolist()

def perform_forecasts_model_2(df, forecast_steps):
    # Model-2'nin tahmin fonksiyonlarını buraya ekleyin
    pass
