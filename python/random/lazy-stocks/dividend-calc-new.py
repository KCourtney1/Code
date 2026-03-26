import yfinance as yf
import pandas as pd

tickers = ["d", "ed", "duk", "dis", "t", "alex", "intc", "aapl", "dow", "nvda", "goog", "FCX", "AEO", "KO", "O", "MO", "VZ", "MSFT", "AVGO", "LYB", "PFE", "LOW", "AVGO"]
cash = 1413.98

def get_dividend(info):
    return info.get('dividendRate') or info.get('trailingAnnualDividendRate') or 0.0

def get_stockPrice(info):
    return info.get("currentPrice") or info.get("regularMarketPreviousClose") or 0.0

rows = []
for symbol in tickers:
    tick = yf.Ticker(symbol)
    info = tick.info

    name = info.get('longName', symbol)
    stock_price = get_stockPrice(info)
    dividend = get_dividend(info)
    print(f"Fetching data for: {symbol}...{name}")

    if dividend == 0:
        print(f"  > NOTE: {symbol} returned a $0.00 dividend (or no data found).")

    shares = cash // stock_price if stock_price > 0 else 0
    income = round(dividend * shares, 2)
    yield_pct = round((dividend / stock_price) * 100, 2) if stock_price > 0 else 0

    rows.append([name, stock_price, shares, income, f"{yield_pct}%"])

columns = ["Company", "Stock Price", "Shares", "Annual Income", "Dividend Yield"]
dividend_table = pd.DataFrame(rows, columns=columns)
try:
    dividend_table.to_excel("dividend_table.xlsx", index=False)
    print("Success! File saved as dividend_table.xlsx")
except ImportError:
    print("Error: Please run 'pip install openpyxl' to save to Excel.")   
