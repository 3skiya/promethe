import tensorflow as tf
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def perform_forecasts_model_2(df, forecast_steps):
    # MinMaxScaler ile veriyi ölçeklendirme
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(df['close'].values.reshape(-1, 1))
    
    # Modeli yükleme
    model = tf.keras.models.load_model('new_models/lstm_model.h5')
    
    # Tahminleri yapma
    predictions = []
    last_data = scaled_data[-60:]
    
    for _ in range(forecast_steps):
        prediction = model.predict(last_data.reshape(1, 60, 1))
        predictions.append(prediction[0][0])
        last_data = np.append(last_data[1:], prediction)
    
    # Tahminleri ölçekten geri çevirme
    predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1))
    return predictions
