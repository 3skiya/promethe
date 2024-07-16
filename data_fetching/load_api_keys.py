# data_fetching/load_api_keys.py

def load_api_keys(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()
        api_key = lines[0].strip().split('=')[1]
        api_secret = lines[1].strip().split('=')[1]
    return api_key, api_secret
