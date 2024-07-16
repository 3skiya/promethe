import configparser

def load_trade_values(file_path):
    config = configparser.ConfigParser()
    try:
        with open(file_path, 'r') as f:
            print(f.read())  # Dosyanın içeriğini ekrana yazdır
            f.seek(0)  # Dosya imlecini başa al
            config.read_file(f)
        if not config.sections() and 'DEFAULT' not in config:
            raise ValueError(f"Config file {file_path} is empty or not formatted correctly.")
        trade_values = {}
        for key in config['DEFAULT']:
            trade_values[key] = config['DEFAULT'][key]
        return trade_values
    except Exception as e:
        raise ValueError(f"Config file {file_path} is empty or not formatted correctly. Error: {e}")

if __name__ == "__main__":
    trade_values_path = '/root/Crypto/Prometheus/TradeValues.txt'
    trade_values = load_trade_values(trade_values_path)
    print(trade_values)
