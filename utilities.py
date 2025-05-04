#Helper Functions
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from datetime import datetime

from os import system, name

# Function to Clear the Screen
def clear_screen():
    if name == "nt": # User is running Windows
        _ = system('cls')
    else: # User is running Linux or Mac
        _ = system('clear')

# Function to sort the stock list (alphabetical)
def sortStocks(stock_list):
    ## Sort the stock list
    stock_list = sorted(stock_list, key=lambda s: s.symbol)
    print("Sorted data based on stock name")


# Function to sort the daily stock data (oldest to newest) for all stocks
def sortDailyData(stock_list):
    stock_list = sorted(
    stock_list,
    key=lambda s: max(
        (datetime.strptime(d.date, "%m-%d-%y") if isinstance(d.date, str) else d.date for d in s.DataList),
        default=datetime.min
    ),
    reverse=True)

# Function to create stock chart
def display_stock_chart(stock_list,symbol):
    plt.close('all')
    plt.figure(figsize=(10, 6))
    found_stock = False
    for stock in stock_list:
        if stock.symbol == symbol:
            found_stock = True
            dates = [d.date for d in stock.DataList]
            closes = [d.close for d in stock.DataList]
            plt.plot(dates, closes, linestyle='dotted', color='gray', linewidth=1)
            plt.scatter(dates, closes, color='red', marker='x', s=100, label=stock.symbol)
            for date, price in zip(dates, closes):
                plt.text(date, price + 0.5, f"{price}", ha='center', fontsize=8, color='black')
            break
    if not found_stock:
        print("Could not find the stock from the stock list, add stock first!\n")
        return
    
    plt.xlabel("Date")
    plt.ylabel("Close Price")
    plt.title(f"{stock.symbol} Stock Prices Over Time")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()