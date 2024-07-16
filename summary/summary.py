def summary_results(trade_list, balance, drawdown, roi, pnl):
    # Burada özet sonuçları hesaplayan ve döndüren kod bulunmalı
    summary = {
        "Total Trades": len(trade_list),
        "Wins": len([trade for trade in trade_list if trade['Profit'] > 0]),
        "Losses": len([trade for trade in trade_list if trade['Profit'] <= 0]),
        "Final Balance": balance,
        "Max Drawdown": drawdown,
        "Total ROI": roi,
        "Total PNL": pnl
    }
    return summary
