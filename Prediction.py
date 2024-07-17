import pandas as pd
import numpy as np

def moving_average(data, window_size):
    data['Prediction'] = data['close'].rolling(window=window_size).mean()
    return data

def exponential_smoothing(data, alpha):
    data['Prediction'] = data['close'].ewm(alpha=alpha).mean()
    return data

def linear_regression(data):
    data['Prediction'] = data[['close']].shift(-1)
    return data

def predict(data, model, **kwargs):
    if model == 'moving_average':
        window_size = kwargs.get('window_size', 3)
        return moving_average(data, window_size)
    elif model == 'exponential_smoothing':
        alpha = kwargs.get('alpha', 0.1)
        return exponential_smoothing(data, alpha)
    elif model == 'linear_regression':
        return linear_regression(data)
    else:
        raise ValueError("Model not recognized")

def main():
    # Örnek veri
    data = pd.DataFrame({
        'close': [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    })

    # Hareketli Ortalama
    ma_prediction = predict(data, 'moving_average', window_size=3)
    print("Hareketli Ortalama Tahmini:\n", ma_prediction)

    # Üstel Düzeltme
    es_prediction = predict(data, 'exponential_smoothing', alpha=0.2)
    print("Üstel Düzeltme Tahmini:\n", es_prediction)

    # Doğrusal Regresyon
    lr_prediction = predict(data, 'linear_regression')
    print("Doğrusal Regresyon Tahmini:\n", lr_prediction)

if __name__ == "__main__":
    main()
