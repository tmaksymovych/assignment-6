import yfinance as yf
import pandas as pd

available_stocks = ["AAPL", "TSLA", "GOOGL", "MSFT", "AMZN"]
stock_name = input(f"Choose one of actions from list: {', '.join(available_stocks)} : ")
while True:
    if stock_name not in available_stocks:
        print("Error: Please choose a stock from the list.")
        stock_name = input(f"Choose one of actions from list: {', '.join(available_stocks)} : ")
    else:
        ticker = yf.Ticker(f"{stock_name}")
        data = ticker.history(period="1y")
        data = data.round(2)
        break
data["Sell"] = False
data["Buy"] = False
data["Hold"] = False

def rolling_mean():
    data["short"] = data["Close"].rolling(window=5).mean()
    data["long"] = data["Close"].rolling(window=20).mean()

    for index in range(20, len(data)):
        if data["short"].iloc[index] > data["long"].iloc[index] and data["short"].iloc[index-1] <= data["long"].iloc[index-1]:
            data.loc[data.index[index], "Buy"] = True
        elif data["short"].iloc[index] < data["long"].iloc[index] and data["short"].iloc[index-1] >= data["long"].iloc[index-1]:
            data.loc[data.index[index], "Sell"] = True
        else:
            data.loc[data.index[index], "Hold"] = True

def run_bot():
        try:
            balance = float(input(f"Sum which you want to deposit:\n"))
        except ValueError:
            print("Invalid input. Enter another sum")
            return
        number_of_stocks = 0
        initial_balance = balance
        for index in range(len(data) - 1):
            if data["Buy"].iloc[index] and balance > 0:
                trade_price = data["Open"].iloc[index+1]
                number_of_stocks = balance / trade_price
                balance = 0
            elif data["Sell"].iloc[index] and number_of_stocks > 0:
                trade_price = data["Open"].iloc[index+1]
                balance = number_of_stocks * trade_price
                number_of_stocks = 0 

        if number_of_stocks > 0:
            final_balance = round(number_of_stocks * data["Close"].iloc[-1],2)
        else:
            final_balance = round(balance,2)
        print(f"Initial balance: {initial_balance}$")
        print(f"Final balance: {final_balance}$")
        profit = round(final_balance - initial_balance,2)
        print(f"Profit: {profit}$")

rolling_mean()
run_bot()
