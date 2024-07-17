import subprocess

try:
    result = subprocess.run(['python3', 'new_models/arima_model.py'], check=True, capture_output=True, text=True)
    print('arima_model_training.py: success')
except subprocess.CalledProcessError as e:
    print(f'arima_model_training.py: fail ({e})')
