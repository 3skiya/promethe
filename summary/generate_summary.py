# summary/generate_summary.py

import pandas as pd

def generate_summary(results):
    trades = []
    for entry, exit in zip(results['entry_points'], results['exit_points']):
        trades.append({
            'Entry Time': entry[0],
            'Exit Time': exit[0],
            'Entry Price': entry[1],
            'Exit Price': exit[1],
            'Profit': exit[1] - entry[1],
            'Direction': 'Long' if entry[1] < exit[1] else 'Short'
        })
    
    trades_df = pd.DataFrame(trades)
    
    summary = {
        'Total Trades': len(trades),
        'Wins': results['num_wins'],
        'Losses': results['num_losses'],
        'Final Balance': results['final_balance'],
        'Max Drawdown': results['max_drawdown'],
        'Total ROI': results['total_roi'],
        'Total PNL': results['total_pnl']
    }
    
    return trades_df, summary
