# config.py
def load_config(filepath):
    config = {}
    with open(filepath, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            config[key] = value.lower() in ['true', '1', 'yes']
    return config
