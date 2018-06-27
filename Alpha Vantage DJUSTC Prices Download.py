import os
import pandas as pd
import alpha_vantage as av
from alpha_vantage.timeseries import TimeSeries
import datetime,time
from datetime import datetime


os.chdir("C:/Users/YJ/Documents/1) Learning/Udacity - Machine Learning/capstone/Submission")
api = input("Please inset the api key: ")

DJUSTC = pd.read_csv("TickerNamesDJUSTC.csv")
tickers = list(DJUSTC.Symbol)
ts = TimeSeries(key=api, output_format='pandas')
output = pd.DataFrame()

for ticker in tickers:
    data, meta_data = ts.get_daily(symbol=ticker, outputsize='full')
    data['ticker'] = ticker
    output = output.append(data.iloc[-1500:])
    print(ticker)
    time.sleep(5)
    
output.to_csv("DJUSTC Prices.csv")