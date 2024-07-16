def summary_results(df, initial_balance):
    total_trades = df[df['signal'] != 'hold'].shape[0]
    wins = df[(df['signal'] != 'hold') & (df['profit'] > 0)].shape[0]
    losses = df[(df['signal'] != 'hold') & (df['profit'] <= 0)].shape[0]
    final_balance = initial_balance + df['profit'].sum()
    max_drawdown = (df['profit'].min() / initial_balance) * 100
    total_roi = ((final_balance - initial_balance) / initial_balance) * 100
    total_pnl = final_balance - initial_balance

    print(f"Total Trades: {total_trades}, Wins: {wins}, Losses: {losses}, Final Balance: ${final_balance:.2f}, Max Drawdown: {max_drawdown:.2f}%, Total ROI: {total_roi:.2f}%, Total PNL: ${total_pnl:.2f}")
