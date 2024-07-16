# performance/print_mape.py

def print_mape(mapes):
    if mapes['arima'] is not None:
        print(f"ARIMA MAPE: {mapes['arima']:.2f}")
    if mapes['prophet'] is not None:
        print(f"Prophet MAPE: {mapes['prophet']:.2f}")
    if mapes['lstm'] is not None:
        print(f"LSTM MAPE: {mapes['lstm']:.2f}")
