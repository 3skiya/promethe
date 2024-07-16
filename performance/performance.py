import numpy as np
def calculate_mape(y_true, y_pred):
    """
    Calculate the Mean Absolute Percentage Error (MAPE)
    :param y_true: array of true values
    :param y_pred: array of predicted values
    :return: MAPE value
    """
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

def print_mape(mape):
    """
    Print the MAPE value
    :param mape: MAPE value to print
    """
    print(f"MAPE: {mape:.2f}%")

def backtest(data, forecasts, initial_balance):
    """
    Backtest a given strategy
    :param data: historical data for backtesting
    :param forecasts: forecasts for the backtest period
    :param initial_balance: starting balance for the backtest
    :return: backtesting results
    """
    # Placeholder implementation, replace with actual backtesting logic
    return {"profit": 0, "trades": 0, "initial_balance": initial_balance}
#v1.1
