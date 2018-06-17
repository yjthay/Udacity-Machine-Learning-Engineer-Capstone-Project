import pandas as pd
import os
import re
import datetime


os.chdir("C:/Users/YJ/Documents/1) Learning/Udacity - Machine Learning/capstone/Submission")

ratios = pd.read_csv("DJUSTC Key Ratios.csv")
ratios.index = ratios[ratios.columns[1]]
ratios = ratios.drop(ratios.columns[[0,1]],axis=1)


prices = pd.read_csv("DJUSTC breakdown.csv")
#prices.date = prices.date.apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d"))
prices.date = pd.to_datetime(prices.date)

output = pd.DataFrame()

for i in range(len(prices)):
    ticker_name = prices.iloc[i].ticker
    year = prices.iloc[i].date.year
    augment = ratios[(ratios.ticker == ticker_name)][[str(year)]].iloc[:,0]
    augment = augment.rename(i)
    #output = pd.DataFrame(prices.iloc[i].append(augment)).transpose()
    #output.to_hdf('DJUSTC Prices and Ratios.h5',"Output",append=True)
    output = output.append(prices.iloc[i].append(augment),ignore_index=True) 
output.to_csv("DJUSTC Prices and Ratios.csv")