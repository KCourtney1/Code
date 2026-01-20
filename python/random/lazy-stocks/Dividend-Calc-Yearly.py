import yfinance as yf
import os,csv

def get_tickers_money(filename):
    target_path = os.path.join(os.path.dirname(__file__),filename)
    with open(target_path,"r") as the_file:
        contents = the_file.readlines()
        money = float(contents[-1])
        tickers = []
        for line in contents:
            line = line.strip()
            line = line.split(",")
            for ticker in line:
                if ticker and ticker[0] not in "1234567890":
                    tickers.append(ticker.strip().upper())
    return tickers, money

def get_stock_prices(ticker):
    stock = yf.Ticker(ticker)
    historical_data = stock.history(period="30m")
    return round(historical_data["Close"].iloc[0],2)

def get_dividend(ticker):
    stock = yf.Ticker(ticker)
    dividends_data = stock.dividends
    if len(dividends_data)>0:
        return dividends_data.iloc[-1]
    else:
        return 0

def get_ticker_info(ticker_money):
    #is given the tuple ticker_money and then returns a dict with the key being the ticker and the value a list[price, shares, dividends, income]
    tickerInfo = {}
    for ticker in ticker_money[0]:
        stockPrice = get_stock_prices(ticker)
        dividendReturn = get_dividend(ticker)
        numberOfShares = ticker_money[1]//stockPrice
        tickerInfo[ticker] = [stockPrice, numberOfShares, dividendReturn, round(dividendReturn*numberOfShares*4,2)]
    return tickerInfo

def write_ticker_info(ticker_info_dic):
    outpath = os.path.join(os.path.dirname(__file__),'lazyStocks.csv')
    with open(outpath,'w' )as out_file:
        out_file.write('Ticker,Stock Price,Shares Buyable,Dividend,Income\n')
        for Key, Value in ticker_info_dic.items():
            out_file.write(f'{Key},{Value[0]},{Value[1]},{Value[2]},{Value[3]}\n')

def main():
    ticker_money = get_tickers_money("stock-test.txt") # gets the tickers[0] and money[1] from a file given stores in a tuple
    ticker_info_dic = get_ticker_info(ticker_money)
    write_ticker_info(ticker_info_dic)

if __name__ == "__main__":
    main()