import subprocess

try:
    result = subprocess.run(['python3', 'new_models/linear_regression_training.py'], check=True, capture_output=True, text=True)
    print('linear_regression_training.py: success')
except subprocess.CalledProcessError as e:
    print(f'linear_regression_training.py: fail ({e})')
