import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

def perform_forecasts_model_5(df, forecast_steps):
    df['date'] = pd.to_datetime(df.index)
    df.set_index('date', inplace=True)
    df = df.asfreq('H')
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(df['close'].values.reshape(-1, 1))
    model = load_model('new_models/gru_wf_model.h5')
    predictions = []
    for i in range(forecast_steps):
        last_data = scaled_data[-60:]
        prediction = model.predict(last_data.reshape(1, 60, 1))
        scaled_data = np.append(scaled_data, prediction, axis=0)
        predictions.append(prediction[0, 0])
    predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1))
    return predictions.flatten()
