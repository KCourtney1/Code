import yfinance as yf
import pandas as pd

tickers = ["d", "ed", "duk", "dis", "t", "alex", "intc", "aapl", "dow", "nvda", "goog"]
cash = 1000.00

def get_dividend(ticker):
    return ticker.info['dividendRate']

def get_stockPrice(ticker):
    return ticker.info["currentPrice"] 

def get_shares(stock_price):
    return cash//stock_price

def get_income(dividend, number_of_shares):
    return round(dividend * number_of_shares * 4, 2)

rows = []
for tick in tickers:
    tick = yf.Ticker(tick)
    stock_price = get_stockPrice(tick)
    dividend = get_dividend(tick)
    shares = get_shares(stock_price)

    rows.append([tick.info['longName'], stock_price, shares, get_income(dividend, shares)])

rows.append(["cash: {}".format(cash)])
dividend_tabel = pd.DataFrame(rows, columns=["ticker", "stock price", "shares", "income"])
dividend_tabel.to_excel("dividend_tabel.xlsx")    
