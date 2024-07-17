import subprocess

# Eğitim dosyalarının yolları
training_files = [
    'new_models/arima_model_training.py',
    'new_models/lstm_model_training.py',
    'new_models/cnn_model_training.py',
    'new_models/gru_model_training.py',
    'new_models/gru_wf_model_training.py',
    'new_models/linear_regression_training.py',
    'new_models/gan_model_training.py'
]

# Eğitim dosyalarını çalıştırma ve sonuçları kontrol etme
for file in training_files:
    try:
        result = subprocess.run(['python3', file], check=True, capture_output=True, text=True)
        print(f'{file}: success')
    except subprocess.CalledProcessError as e:
        print(f'{file}: fail ({e.stderr})')

print("Eğitim dosyaları çalıştırıldı.")
