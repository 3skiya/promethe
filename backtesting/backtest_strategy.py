def backtest_strategy(df):
    initial_balance = 1000
    balance = initial_balance
    positions = []
    entry_points = []
    exit_points = []
    cumulative_returns = []

    for index, row in df.iterrows():
        if row['signal'] == 'buy':
            positions.append({'entry_price': row['close'], 'timestamp': row['timestamp'], 'direction': 'long'})
            entry_points.append((row['timestamp'], row['close']))
        elif row['signal'] == 'sell' and positions:
            position = positions.pop()
            if position['direction'] == 'long':
                profit = row['close'] - position['entry_price']
                balance += profit
                exit_points.append((row['timestamp'], row['close']))
        
        cumulative_returns.append(balance - initial_balance)

    df['cumulative_returns'] = cumulative_returns

    results = {
        'df': df,
        'final_balance': balance,
        'max_drawdown': min(cumulative_returns),
        'num_trades': len(entry_points),
        'num_wins': sum(1 for e, x in zip(entry_points, exit_points) if x[1] > e[1]),
        'num_losses': sum(1 for e, x in zip(entry_points, exit_points) if x[1] <= e[1]),
        'total_roi': (balance - initial_balance) / initial_balance,
        'total_pnl': balance - initial_balance,
        'open_positions': len(positions),
        'entry_points': entry_points,
        'exit_points': exit_points,
        'cumulative_returns': cumulative_returns,
    }

    return results
