import subprocess

try:
    result = subprocess.run(['python3', 'new_models/lstm_model.py'], check=True, capture_output=True, text=True)
    print('lstm_model_training.py: success')
except subprocess.CalledProcessError as e:
    print(f'lstm_model_training.py: fail ({e})')
