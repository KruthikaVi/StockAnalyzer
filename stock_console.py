# Summary: This module contains the user interface and logic for a console-based version of the stock manager program.

from datetime import datetime
from stock_class import Stock, DailyData
from utilities import clear_screen, display_stock_chart
from os import path
import shutil
import stock_data


def main_menu(stock_list):
    clear_screen()
    header()
    while True:
        print("Stock Analyzer main menu---")
        print("1 - Manage Stocks (Add, Update, Delete, List)")
        print("2 - Add Daily Stock Data (Date, Price, Volume)")
        print("3 - Show Report")
        print("4 - Show Chart")
        print("5 - Manage Data (Save, Load, Retrieve)")
        print("0 - Exit Program")
        option = input("Enter your Choice: ")
        if option=="1":
            manage_stocks(stock_list)
        elif option == "2":
            add_stock_data(stock_list)
        elif option == "3":
            display_report(stock_list)
        elif option == "4":
            display_chart(stock_list)
        elif option == "5":
            manage_data(stock_list)
        elif option=="0":
            clear_screen()
            print("Goodbye")
            break
        else:
            clear_screen()
            print("*** Invalid Option - Try again ***\n")

# Manage Stocks
def manage_stocks(stock_list):
    clear_screen()
    header()
    try:
        while True:
            print("1 - Add Stock")
            print("2 - Update Shares")
            print("3 - Delete Stock")
            print("4 - List Stocks")
            print("0 - Exit Manage Stocks")
            print("Manage Stocks ---")
            option = input("Enter Menu Option: ")
            if option == "1":
                add_stock(stock_list)
            elif option == "2":
                update_shares(stock_list)
            elif option == "3":
                delete_stock(stock_list)
            elif option == "4":
                list_stocks(stock_list)
            elif option == "0":
                clear_screen()
                header()
                print("Returning to Main Menu\n")
                break
            else:
                clear_screen()
                header()
                print("*** Invalid Option - Try again ***\n")
    except Exception as e:
            print(f"Error managing the stocks {str(e)}")

# Add new stock to track
def add_stock(stock_list):
    clear_screen()
    header()
    print("Add stock data")
    symbol = input("Enter Ticker Symbol: ")
    try:
        for stock in stock_list:
            if stock.symbol == symbol:
                print("Stock already exists, buy stock instead!\n")
                return
        name = input("Enter Company Name: ")
        quantity = input("Enter Number of shares ")
        new_stock = Stock(symbol,name,int(quantity))
        stock_list.append(new_stock)
        stock_data.save_stock_data(stock_list)
        stock_data.load_stock_data(stock_list)
        print(f"{quantity} Stocks for {symbol} added successfully\n")
    except Exception as e:
            print(f"Error Adding the stocks {str(e)}")
        
# Buy or Sell Shares Menu
def update_shares(stock_list):
    clear_screen()
    header()
    try:
        while True:
            print("1 - Buy shares")
            print("2 - Sell Shares")
            print("0 - Exit Update Shares")
            option = input("Enter your option: ")
            if option == "1":
                buy_stock(stock_list)
            elif option=="2":
                 sell_stock(stock_list)
            elif option=="0":
                 print("Exiting Update shares options!\n")
                 break
            else:
                print("*** Invalid Option - Try again ***\n")
    except Exception as e:
            print(f"Error updating the shares {str(e)}")

# Buy Stocks (add to shares)
def buy_stock(stock_list):
    clear_screen()
    header()
    print("Buy Shares ---")
    try:
        symbols = [stock.symbol for stock in stock_list]
        print(f"Stock List: {symbols}")
        symbol = input("Which stock do you want to buy?: ")
        quantity = input("How many shares do you want to buy?: ")
        found_stock = False
        for stock in stock_list:
            if stock.symbol == symbol:
                found_stock = True
                stock.buy(int(quantity))
                stock_data.save_stock_data(stock_list)
                stock_data.load_stock_data(stock_list)
                print(f"{quantity} new {symbol} Stocks added, total stocks now {stock.shares}!\n")
                break
        if not found_stock:
             print("Could not find the stock from the stock list\n")
    except Exception as e:
            print(f"Error purchasing the shares {str(e)}")

# Sell Stocks (subtract from shares)
def sell_stock(stock_list):
    clear_screen()
    header()
    print("Sell Shares ---")
    try:
        symbols = [stock.symbol for stock in stock_list]
        print(f"Stock List: {symbols}")
        symbol = input("Which stock do you want to sell?: ")
        quantity = input("How many shares do you want to sell?: ")
        found_stock = False
        for stock in stock_list:
            if stock.symbol == symbol:
                found_stock = True
                if stock.shares >= int(quantity):
                    stock.sell(int(quantity))
                    stock_data.save_stock_data(stock_list)
                    stock_data.load_stock_data(stock_list)
                    print(f"{quantity} stocks of {symbol} sold, total stocks now {stock.shares}!\n")
                else:
                        print(f"Not enough stocks to sell, current holding - {stock.shares}")
                break
        if not found_stock:
             print("Could not find the stock from the stock list")       
    except Exception as e:
            print(f"Error selling the shares {str(e)}")

# Remove stock and all daily data
def delete_stock(stock_list):
    clear_screen()
    header()
    print("Delete Shares ---")
    try:
        symbols = [stock.symbol for stock in stock_list]
        print(f"Stock List: {symbols}")
        symbol = input("Enter the stock symbol to delete: ")
        found_stock = False
        for stock in stock_list:
            if stock.symbol == symbol:
                found_stock = True
                stock_data.delete_stock_data(symbol)
                stock_data.load_stock_data(stock_list)
                print("Deleted stock data successfully!")
        if not found_stock:
             print("Could not find the stock from the stock list")
    except Exception as e:
            print(f"Error deleting the stock {str(e)}")


# List stocks being tracked
def list_stocks(stock_list):
    clear_screen()
    header()
    print("List Stocks ---\n")
    try:
        stock_data.load_stock_data(stock_list)
        print("=== Stock Table ===\n")
        print(f"{'Symbol':<10} {'Name':<20} {'Quantity':<10}")
        print("-" * 60)
        for stock in stock_list:
                print(f"{stock.symbol:<10} {stock.name:<20} {stock.shares:<10}\n")
    except Exception as e:
            print(f"Error listing the stocks {str(e)}")

# Add Daily Stock Data
def add_stock_data(stock_list):
    clear_screen()
    header()
    print("Add Daily Stock Data")
    try:
        symbols = [stock.symbol for stock in stock_list]
        print(f"Stock List: {symbols}")
        symbol = input("Enter stock symbol to update: ")
        found_stock = False
        for stock in stock_list:
            if stock.symbol == symbol:
                found_stock = True
                date = input("Enter Date (MM/DD/YY): ")
                price = input("Enter Price: ")
                volume = input("Enter Volume: ")
                daily_data = DailyData(datetime.strptime(date,"%m/%d/%y"),float(price),float(volume))
                stock.add_data(daily_data)
                stock_data.save_stock_data(stock_list)
                stock_data.load_stock_data(stock_list)
                print("Daily data added successfully!\n")
                return
        if not found_stock:
             print("Could not find the stock from the stock list, add stock first!\n")
    except Exception as e:
            print(f"Error adding daily stock data {str(e)}")

# Display Report for All Stocks
def display_report(stock_list):
    clear_screen()
    header()
    print("---- Stock Report ----\n")
    try:
        for stock in stock_list:
            print(f"\n{'Symbol':<10} {'Name':<20} {'Quantity':<10}")
            print("-" * 60)
            print(f"{stock.symbol:<10} {stock.name:<20} {stock.shares:<10}\n")
            if not stock.DataList:
                 print(f" No daily data available for {stock.symbol}.")
            else:
                print(f"=== Daily Data for {stock.symbol} ===\n")
                print(f"{'Date':<15} {'Close Price':<20} {'Volume':<10}")
                print("-" * 40)
                for daily in stock.DataList:
                    print(f"{daily.date.strftime('%m/%d/%y'):<15} {daily.close:<20} {daily.volume:<10}\n")
                print("-_-"*40)
        print("\n ---- End of stock report ----- \n")
    except Exception as e:
            print(f"Error displaying the report {str(e)}")

  
# Display Chart
def display_chart(stock_list):
    clear_screen()
    header()
    print("Display Chart \n")
    try:
        symbols = [stock.symbol for stock in stock_list]
        print(f"Stock List: {symbols}")
        symbol = input("Enter stock symbol to view the graph: ")
        display_stock_chart(stock_list, symbol)
    except Exception as e:
            print(f"Error displaying the chart {str(e)}")

# Manage Data Menu
def manage_data(stock_list):
    clear_screen()
    header()
    try:
        while True:
            print("1 - Save Data to Database")
            print("2 - Load Data from Database")
            print("3 - Retrieve Data from Web")
            print("4 - Import from CSV File")
            print("0- Exit Manage Data")
            option = input("Enter your option: ")
            if option =="1":
                clear_screen()
                header()
                stock_data.save_stock_data(stock_list)
                print("Data saved successfully to database!\n")
            elif option =="2":
                clear_screen()
                header()
                stock_data.load_stock_data(stock_list)
                print("Data loaded successfully from Database\n")
            elif option == "3":
                clear_screen()
                header()
                retrieve_from_web(stock_list)
            elif option == "4":
                clear_screen()
                header()
                import_csv(stock_list)
            elif option =="0":
                clear_screen()
                header()
                print("Exiting from Manage Data!\n")
                break
            else:
                 print("*** Invalid Option - Try again ***\n")
    except Exception as e:
            print(f"Error in managing data function {str(e)}")

# Get stock price and volume history from Yahoo! Finance using Web Scraping
def retrieve_from_web(stock_list):
    clear_screen()
    header()
    from_date = input("Enter starting date (MM/DD/YY): ")
    to_date = input("Enter ending date (MM/DD/YY): ")
    try:
        result = stock_data.retrieve_stock_web(from_date, to_date, stock_list)
        stock_data.save_stock_data(stock_list)
        stock_data.load_stock_data(stock_list)
        print(f"Records Retrieved: {str(result)} \n")
    except Exception as e:
            print(f"Error retrieving the data {str(e)}")
    pass

# Import stock price and volume history from Yahoo! Finance using CSV Import
def import_csv(stock_list):
    clear_screen()
    header()
    try:
        symbols = [stock.symbol for stock in stock_list]
        print(f"Stock List: {symbols}")
        symbol = input("Enter stock symbol to import from CSV: ")
        file_path = input("Enter filename of stock to import: ")
        result = stock_data.import_stock_web_csv(stock_list, symbol, file_path)
        stock_data.save_stock_data(stock_list)
        stock_data.load_stock_data(stock_list)
    except Exception as e:
            print(f"Error importing the data {str(e)}")


def header():
        columns = shutil.get_terminal_size().columns
        print("=================================".center(columns))
        print("Welcome to Stock Analyzer".center(columns))
        print("Manage your portfolio".center(columns))
        print("================================".center(columns))
        
# Begin program
def main():
    #check for database, create if not exists
    if path.exists("stocks.db") == False:
        stock_data.create_database()
    stock_list = []
    stock_data.load_stock_data(stock_list)
    main_menu(stock_list)

# Program Starts Here
if __name__ == "__main__":
    # execute only if run as a stand-alone script
    main()