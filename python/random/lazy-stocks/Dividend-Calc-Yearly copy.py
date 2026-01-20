import yfinance as yf
import os,csv

class ticker:

    CASH = 1000.0
    
    def __init__(self, name) -> None:
        self.name = name
        self.stock_prices = round(yf.Ticker(self.name).history(period="1m")["Close"].iloc[0],2)
        if len(yf.Ticker(self.name).dividends)>0:
             self.dividend = yf.Ticker(self.name).dividends.iloc[-1]
        else:
             self.dividend = 0

    @property
    def get_numberOfShares(self):
        return self.CASH//self.stock_prices
    
    @property
    def get_income(self):
        return round(self.dividend*self.get_numberOfShares*4,2)
        
    def __str__(self) -> str:
        return f"{self.name}"
    __repr__ = __str__
        
def get_tickers(filename):
    target_path = os.path.join(os.path.dirname(__file__),filename)
    with open(target_path,"r") as the_file:
        contents = the_file.read().split()
        tickers = []
        for item in contents:
            tickers.append(ticker(item.strip(",").upper()))
    return tickers

def main():
    ticker_list = get_tickers("stock-test copy.txt") # gets the tickers[0] and money[1] from a file given stores in a tuple
    ticker.CASH = 2000
    

if __name__ == "__main__":
    main()