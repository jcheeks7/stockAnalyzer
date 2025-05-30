
import yfinance as yf
import matplotlib.pyplot as plt

def backtest(ticker, start_date, end_date, strategy):
    data = yf.download(ticker, start=start_date, end=end_date)
    signals = strategy(data)
    portfolio = 10000  # Starting balance
    positions = 0
    cash = portfolio
    portfolio_values = []

    for i in range(len(data)):
        price = data['Close'].iloc[i]
        if signals[i] == 'BUY':
            shares = cash // price
            cash -= shares * price
            positions += shares
        elif signals[i] == 'SELL' and positions > 0:
            cash += positions * price
            positions = 0
        total_value = cash + positions * price
        portfolio_values.append(total_value)

    plt.plot(data.index, portfolio_values)
    plt.title(f"Backtest of {ticker}")
    plt.show()
