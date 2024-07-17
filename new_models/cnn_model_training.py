import subprocess

try:
    result = subprocess.run(['python3', 'new_models/cnn_model_training.py'], check=True, capture_output=True, text=True)
    print('cnn_model_training.py: success')
except subprocess.CalledProcessError as e:
    print(f'cnn_model_training.py: fail ({e})')
