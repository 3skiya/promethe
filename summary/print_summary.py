# summary/print_summary.py

def print_summary(trades_df, summary):
    print("Trade List:")
    print(trades_df)
    print("="*33)
    print(f"Total Trades: {summary['Total Trades']}")
    print(f"Wins: {summary['Wins']}")
    print(f"Losses: {summary['Losses']}")
    print(f"Final Balance: {summary['Final Balance']:.2f}")
    print(f"Max Drawdown: {summary['Max Drawdown']:.2f}")
    print(f"Total ROI: {summary['Total ROI']*100:.2f}%")
    print(f"Total PNL: {summary['Total PNL']:.2f}")
