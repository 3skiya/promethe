class PredictionModels:
    def __init__(self, data):
        self.data = data
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.data_scaled = self.scaler.fit_transform(self.data['close'].values.reshape(-1, 1))

    def arima_model(self, order=(5, 1, 0)):
        model = ARIMA(self.data['close'], order=order)
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=10)
        return forecast

    def lstm_model(self, model_path='models/lstm_model.h5'):
        model = load_model(model_path)
        prediction_days = 60
        x_test = []
        for x in range(prediction_days, len(self.data_scaled)):
            x_test.append(self.data_scaled[x-prediction_days:x, 0])
        x_test = np.array(x_test)
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
        predictions = model.predict(x_test)
        predictions = self.scaler.inverse_transform(predictions)
        return predictions

    def cnn_model(self, model_path='models/cnn_model.h5'):
        model = load_model(model_path)
        prediction_days = 60
        x_test = []
        for x in range(prediction_days, len(self.data_scaled)):
            x_test.append(self.data_scaled[x-prediction_days:x, 0])
        x_test = np.array(x_test)
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
        predictions = model.predict(x_test)
        predictions = self.scaler.inverse_transform(predictions)
        return predictions

    def evaluate_model(self, true_values, predictions):
        mse = np.mean((true_values - predictions) ** 2)
        rmse = np.sqrt(mse)
        mae = np.mean(np.abs(true_values - predictions))
        mape = np.mean(np.abs((true_values - predictions) / true_values)) * 100
        return {'MSE': mse, 'RMSE': rmse, 'MAE': mae, 'MAPE': mape}
