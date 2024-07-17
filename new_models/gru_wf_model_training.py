import subprocess

try:
    result = subprocess.run(['python3', 'new_models/gru_wf_model_training.py'], check=True, capture_output=True, text=True)
    print('gru_wf_model_training.py: success')
except subprocess.CalledProcessError as e:
    print(f'gru_wf_model_training.py: fail ({e})')
