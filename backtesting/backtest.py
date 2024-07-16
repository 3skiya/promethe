import pandas as pd

def backtest(df, forecasts, initial_balance):
    balance = initial_balance
    trades = 0
    wins = 0
    losses = 0
    max_drawdown = 0
    pnl = 0
    roi = 0
    drawdown = 0

    for i in range(len(df)):
        if df.loc[i, 'signal'] == 'buy':
            buy_price = df.loc[i, 'close']
            balance -= buy_price
            trades += 1

        elif df.loc[i, 'signal'] == 'sell':
            sell_price = df.loc[i, 'close']
            balance += sell_price
            trades += 1
            if sell_price > buy_price:
                wins += 1
                pnl += sell_price - buy_price
            else:
                losses += 1
                pnl += sell_price - buy_price

        current_drawdown = (initial_balance - balance) / initial_balance * 100
        if current_drawdown > max_drawdown:
            max_drawdown = current_drawdown

    roi = pnl / initial_balance * 100

    results = {
        'Total Trades': trades,
        'Wins': wins,
        'Losses': losses,
        'Final Balance': balance,
        'Max Drawdown': max_drawdown,
        'Total ROI': roi,
        'Total PNL': pnl
    }

    return results
