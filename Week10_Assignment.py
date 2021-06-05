"""
Author:    Darien Bernal
e-mail:    darien.bernal@du.edu
Date:      5/30/2021
Version:   1.0
Code Purpose:
The code calculates the total value of each stock and plots a line graph using a json file.
Code Inputs:
The inputs comes from a json file, which includes information about each stock on each day
in the portfolio. This includes symbol, date, open price, close price, high, low and volume.
Code Output:
The code outputs a database, table and line graph.
"""

import json, csv
import pandas as pd
import sqlite3, matplotlib.pyplot as plt
import datetime

# Sets json file to a variable.
file_path = 'AllStocks.json'
with open(file_path) as f:
    all_stock_data = json.load(f)

#Lists contains stock information
stock_symbols = ['googl', 'msft', 'rds-a', 'aig', 'fb', 'm', 'f', 'ibm']
num_shares = [125, 85, 400, 235, 150, 425, 85, 80]
buy_price = [772.88, 56.60, 49.58, 54.21, 124.31, 30.30, 12.58, 150.37]
current_price = [941.53, 73.04, 55.74, 65.27, 175.45, 23.98, 10.98, 145.30]

# Creates empty lists for data.
g_dates = []
g_values = []
msft_dates = []
msft_values = []
rds_dates = []
rds_values = []
aig_dates = []
aig_values = []
fb_dates = []
fb_values = []
m_dates = []
m_values = []
f_dates = []
f_values = []
ibm_dates = []
ibm_values = []

# Adds number of shares for each stock to dictionary as key-value pair
for stock in all_stock_data:
    if stock['Symbol'] == 'GOOG':
        stock['Num_shares']='125'
    elif stock['Symbol'] == 'MSFT':
        stock['Num_shares']='85'
    elif stock['Symbol'] == 'RDS-A':
        stock['Num_shares']='400'
    elif stock['Symbol'] == 'AIG':
        stock['Num_shares']='235'
    elif stock['Symbol'] == 'FB':
        stock['Num_shares']='150'
    elif stock['Symbol'] == 'M':
        stock['Num_shares']='425'
    elif stock['Symbol'] == 'F':
        stock['Num_shares']='85'
    elif stock['Symbol'] == 'IBM':
        stock['Num_shares']='80'

# Creates Stock class.
class Stock:

    def __init__(self, symbol, date, at_open, high, low, close, volume, num_shares):
        self.symbol = symbol
        self.date = date
        self.open = at_open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.num_shares = num_shares

    #Calculates the value of the stock
    def get_values(self):
        value = float(stock['Close']) * int(stock['Num_shares'])
        return value

# Formats data and sets to variable.
for stock in all_stock_data:
    portfolio = Stock(stock['Symbol'], stock['Date'], stock['Open'], stock['High'], stock['Low'], stock['Close'], stock['Volume'], stock['Num_shares'])

# Method calculates value of each stock and adds it to the dictionary.
for stock in all_stock_data:
    stock['Value']=portfolio.get_values()


#Gets the name of the user
name = input("Enter your name: ")

#Prints welcomes message with user name
print(f"\nWelcome, {name.title()}!\n")

#Prints headers for table
print("Stock Symbol \tNo. Shares \tPurchase Price \tCurrent Value")

#Loops through each list and prints information on different lines of the table
for i in range(len(stock_symbols)):
    print(f"{stock_symbols[i].upper()} \t\t{num_shares[i]} \t\t{buy_price[i]} \t\t{current_price[i]}")



#Empty list for math results for each stock
profits = []

#Prompts for program to calculate and print all the user's stocks
portfolio = input("\nWould you like to check your entire portfolio's profits? Yes or No: ")
#User respond "yes" to check entire portfolio
if portfolio.lower() == "yes":
    # Asks user for type of output for information
    print("\nOkay, great!")
    print("\nWould you like to have this information in a table or graph format?")
    graph = input("\nPlease enter 'table' or 'line': ")
    # User wants to receive a table
    if graph.lower() == "table":
        #Prints table headers
        print(f"\nStock ownership for {name.title()}")
        print("Stock \tShare # \tEarnings/Loss")
        #Calculates the gains or loss for each stock
        for s in range(len(stock_symbols)):
            total_purchase = float(buy_price[s]) * float(num_shares[s])
            total_current = float(current_price[s]) * float(num_shares[s])
            gains_loss = float(total_current) - float(total_purchase)
            high_increase = gains_loss / num_shares[s]
            #Prints stocks, shares and resulting gains or loss into table
            print(f"{stock_symbols[s].upper()} \t{num_shares[s]} \t\t${gains_loss:.2f}")
            #Adds results to empty profits list
            profits.append(profits)

        #Finds the index of the highest number in the profits list
        high_gain = profits.index(max(profits))
        #Prints stock with most gain per share if all stocks are profiting
        if gains_loss > 0:
            print(f"\nThe stock with the highest increase in value in your portfolio on a per-share basis is: {stock_symbols[high_gain].upper()}")
        #Prints stock with the least loss if profits are in the negatives
        elif gains_loss < 0:
            print(f"\nThe stock with least decrease in value in your portfolio on a per-share basis is: {stock_symbols[high_gain].upper()}")

    # User wants to receive a line graph
    elif graph.lower() == "line":
        #Declare variable, connect to a database.
        try:
            conn = sqlite3.connect('Week10_Stocks.db')
            print("Opened database successfully.")
        except Error as e:
            print(e)
        finally:
            cursor = conn.cursor()
            conn.execute("CREATE TABLE stocks (symbol TEXT, date DATE, open FLOAT, high FLOAT, low FLOAT, close FLOAT, volume INTEGER, num_shares INTEGER, value FLOAT)")
            print("Table created.")
            for stock in all_stock_data:
                cursor.execute("INSERT INTO stocks VALUES (?,?,?,?,?,?,?,?,?)", (stock['Symbol'], stock['Date'], 
                stock['Open'], stock['High'], stock['Low'], stock['Close'], stock['Volume'], stock['Num_shares'], 
                stock['Value']))
            print("Table data inserted.\n\n")

        # Loads each list with the date and total stock value.
            cursor.execute("SELECT date, value FROM stocks WHERE symbol='GOOG'")
            stocks = cursor.fetchall()
            for goog in stocks:
                orig_date = goog[0]
                new_date = datetime.datetime.strptime(orig_date, '%d-%b-%y')
                g_dates.append(new_date.strftime('%m-%d-%y'))
                g_values.append(goog[1])

            cursor.execute("SELECT date, value FROM stocks WHERE symbol='MSFT'")
            stocks = cursor.fetchall()
            for msft in stocks:
                orig_date = msft[0]
                new_date = datetime.datetime.strptime(orig_date, '%d-%b-%y')
                msft_dates.append(new_date.strftime('%m-%d-%y'))
                msft_values.append(msft[1])

            cursor.execute("SELECT date, value FROM stocks WHERE symbol='RDS-A'")
            stocks = cursor.fetchall()
            for rds in stocks:
                orig_date = rds[0]
                new_date = datetime.datetime.strptime(orig_date, '%d-%b-%y')
                rds_dates.append(new_date.strftime('%m-%d-%y'))
                rds_values.append(rds[1])

            cursor.execute("SELECT date, value FROM stocks WHERE symbol='AIG'")
            stocks = cursor.fetchall()
            for aig in stocks:
                orig_date = aig[0]
                new_date = datetime.datetime.strptime(orig_date, '%d-%b-%y')
                aig_dates.append(new_date.strftime('%m-%d-%y'))
                aig_values.append(aig[1])

            cursor.execute("SELECT date, value FROM stocks WHERE symbol='FB'")
            stocks = cursor.fetchall()
            for fb in stocks:
                orig_date = fb[0]
                new_date = datetime.datetime.strptime(orig_date, '%d-%b-%y')
                fb_dates.append(new_date.strftime('%m-%d-%y'))
                fb_values.append(fb[1])

            cursor.execute("SELECT date, value FROM stocks WHERE symbol='M'")
            stocks = cursor.fetchall()
            for m in stocks:
                orig_date = m[0]
                new_date = datetime.datetime.strptime(orig_date, '%d-%b-%y')
                m_dates.append(new_date.strftime('%m-%d-%y'))
                m_values.append(m[1])

            cursor.execute("SELECT date, value FROM stocks WHERE symbol='F'")
            stocks = cursor.fetchall()
            for f in stocks:
                orig_date = f[0]
                new_date = datetime.datetime.strptime(orig_date, '%d-%b-%y')
                f_dates.append(new_date.strftime('%m-%d-%y'))
                f_values.append(f[1])

            cursor.execute("SELECT date, value FROM stocks WHERE symbol='IBM'")
            stocks = cursor.fetchall()
            for ibm in stocks:
                orig_date = ibm[0]
                new_date = datetime.datetime.strptime(orig_date, '%d-%b-%y')
                ibm_dates.append(new_date.strftime('%m-%d-%y'))
                ibm_values.append(ibm[1])


        # Styles line graph
            plt.style.use('seaborn')

        # Plots the points onto the line graph.
            fig, ax = plt.subplots()
            ax.plot(g_dates, g_values, c='red')
            ax.plot(msft_dates, msft_values, c='blue')
            ax.plot(rds_dates, rds_values, c='pink')
            ax.plot(aig_dates, aig_values, c='gray')
            ax.plot(fb_dates, fb_values, c='orange')
            ax.plot(m_dates, m_values, c='green')
            ax.plot(f_dates, f_values, c='purple')
            ax.plot(ibm_dates, ibm_values, c='yellow')

        # Labels the line graph, x-axis and y-xis.
            ax.set_title(f"Value of {name.title()}'s Stock Portfolio", fontsize=18)
            ax.set_xlabel('Date', fontsize=10)
            fig.autofmt_xdate()
            ax.set_ylabel("Stock Value", fontsize=14)
            ax.tick_params(axis='both', labelsize=10)

        # Sets number of dates on displays on the x-axis.
            ax.xaxis.set_ticks([0,25,50,75,100,125,150,175,200,225,250,275,300,
            325,350,375,400,425,450,475,500])

        # Shows line graph.
            plt.show()

#Programs prints goodbye message and ends after user inputs "no"
elif portfolio.lower() == "no":
    print("Okay, have a great day!")