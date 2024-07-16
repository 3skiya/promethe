import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
import pickle

def perform_forecasts_model_1(df, forecast_steps):
    df['date'] = pd.to_datetime(df.index)
    df.set_index('date', inplace=True)
    df = df.asfreq('H')
    model = ARIMA(df['close'], order=(5, 1, 0))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=forecast_steps)
    return forecast

def perform_forecasts_model_2(df, forecast_steps):
    df['date'] = pd.to_datetime(df.index)
    df.set_index('date', inplace=True)
    df = df.asfreq('H')
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(df['close'].values.reshape(-1, 1))
    model = load_model('new_models/lstm_model.h5')
    predictions = []
    for i in range(forecast_steps):
        last_data = scaled_data[-60:]
        prediction = model.predict(last_data.reshape(1, 60, 1))
        scaled_data = np.append(scaled_data, prediction, axis=0)
        predictions.append(prediction[0, 0])
    predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1))
    return predictions.flatten()

def perform_forecasts_model_3(df, forecast_steps):
    df['date'] = pd.to_datetime(df.index)
    df.set_index('date', inplace=True)
    df = df.asfreq('H')
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(df['close'].values.reshape(-1, 1))
    model = load_model('new_models/cnn_model.h5')
    predictions = []
    for i in range(forecast_steps):
        last_data = scaled_data[-60:]
        prediction = model.predict(last_data.reshape(1, 60, 1))
        scaled_data = np.append(scaled_data, prediction, axis=0)
        predictions.append(prediction[0, 0])
    predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1))
    return predictions.flatten()

def perform_forecasts_model_4(df, forecast_steps):
    df['date'] = pd.to_datetime(df.index)
    df.set_index('date', inplace=True)
    df = df.asfreq('H')
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(df['close'].values.reshape(-1, 1))
    model = load_model('new_models/gru_model.h5')
    predictions = []
    for i in range(forecast_steps):
        last_data = scaled_data[-60:]
        prediction = model.predict(last_data.reshape(1, 60, 1))
        scaled_data = np.append(scaled_data, prediction, axis=0)
        predictions.append(prediction[0, 0])
    predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1))
    return predictions.flatten()

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

def perform_forecasts_model_6(df, forecast_steps):
    df['date'] = pd.to_datetime(df.index)
    df.set_index('date', inplace=True)
    df = df.asfreq('H')
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(df['close'].values.reshape(-1, 1))
    model_path = 'new_models/linear_regression_model.pkl'
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
    predictions = []
    for i in range(forecast_steps):
        last_data = np.arange(len(scaled_data) + i).reshape(-1, 1)
        prediction = model.predict(last_data[-1].reshape(-1, 1))
        scaled_data = np.append(scaled_data, prediction, axis=0)
        predictions.append(prediction[0, 0])
    predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1))
    return predictions.flatten()

def perform_forecasts_model_7(df, forecast_steps):
    df['date'] = pd.to_datetime(df.index)
    df.set_index('date', inplace=True)
    df = df.asfreq('H')
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(df['close'].values.reshape(-1, 1))
    generator = load_model('new_models/gan_generator.h5')
    predictions = []
    for _ in range(forecast_steps):
        noise = np.random.normal(0, 1, (1, 100))
        prediction = generator.predict(noise)
        scaled_data = np.append(scaled_data, prediction, axis=0)
        predictions.append(prediction[0, 0])
    predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1))
    return predictions.flatten()
