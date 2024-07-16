# train_lstm_model.py dosyasındaki ilgili kodu güncelleyin

# ... (Diğer kodlar)
df = fetch_data(symbol, timeframe, start_date, end_date)
df['close'] = df['close'].astype(float)

scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(df['close'].values.reshape(-1, 1))

# Eğitim ve test verilerinin oluşturulması
train_data = scaled_data[:int(len(scaled_data) * 0.8)]
test_data = scaled_data[int(len(scaled_data) * 0.8):]

x_train, y_train = create_dataset(train_data, 60)
x_test, y_test = create_dataset(test_data, 60)

x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

# Model eğitimi
model = create_lstm_model()
model.fit(x_train, y_train, epochs=10, batch_size=32)
model.save('new_models/lstm_model.h5')
