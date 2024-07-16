import pandas as pd

def backtest(df, forecasts, initial_balance, model_name):
    balance = initial_balance
    trade_list = []
    total_trades = 0
    wins = 0
    losses = 0
    max_drawdown = 0
    highest_balance = balance

    # Gün gün backtest
    for i in range(min(len(df), len(forecasts['lstm']))):  # Uzunluk farkını göz önünde bulundurma
        date = df.index[i]
        rsi = df['rsi'].iloc[i]
        close_price = df['close'].iloc[i]
        forecast_price = forecasts['lstm'][i]

        # İşlem sinyali kontrolü
        signal = 'No Trade'
        if rsi < 30 and forecast_price > close_price:
            signal = 'buy'
            total_trades += 1
            # Alım işlemi gerçekleştir
            # Örneğin, tüm bakiyeyi kullanarak alım yapalım
            amount = balance / close_price
            balance = 0
        elif rsi > 70 and forecast_price < close_price:
            signal = 'sell'
            total_trades += 1
            # Satış işlemi gerçekleştir
            # Örneğin, tüm varlığı satalım
            balance = amount * close_price
            amount = 0

        # İşlem sonucunu kaydet
        if signal != 'No Trade':
            trade_list.append({
                'date': date,
                'rsi': rsi,
                'close_price': close_price,
                'forecast_price': forecast_price,
                'signal': signal,
                'balance': balance
            })

        # Max drawdown hesaplama
        if balance > highest_balance:
            highest_balance = balance
        drawdown = (highest_balance - balance) / highest_balance
        if drawdown > max_drawdown:
            max_drawdown = drawdown

        # Günlük sonuçları ekrana yazdırma
        rsi_display = f"{rsi:.2f}" if pd.notna(rsi) else "Hesaplanmadı"
        print(f"{date.date()}")
        print(f"RSI: {rsi_display}")
        print(f"Price: ${close_price:,.2f}")
        print(f"Forecast: ${forecast_price[0]:,.2f}")  # İki ondalık basamakla formatlama
        print(f"Result: {signal}")
        print(f"Total Trades: {total_trades}, Wins: {wins}, Losses: {losses}, Final Balance: ${balance:,.2f}, Max Drawdown: {max_drawdown:.2%}, Total ROI: {(balance - initial_balance) / initial_balance * 100:.2f}%, Total PNL: ${balance - initial_balance:,.2f}")
        print(f"Kullanılan Model: {model_name}")
        print("-" * 50)

    return {
        'Total Trades': total_trades,
        'Wins': wins,
        'Losses': losses,
        'Final Balance': balance,
        'Max Drawdown': max_drawdown,
        'Total ROI': (balance - initial_balance) / initial_balance * 100,
        'Total PNL': balance - initial_balance
    }
