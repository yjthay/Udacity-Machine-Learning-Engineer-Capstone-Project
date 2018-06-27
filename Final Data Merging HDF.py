import pandas as pd
import os
import re
import datetime


os.chdir("C:/Users/YJ/Documents/1) Learning/Udacity - Machine Learning/capstone/Submission")

ratios = pd.read_csv("DJUSTC Key Ratios.csv")
ratios.index = ratios[ratios.columns[1]]
ratios = ratios.drop(ratios.columns[[0,1]],axis=1)


prices = pd.read_csv("DJUSTC Prices.csv")
#prices.date = prices.date.apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d"))
prices.date = pd.to_datetime(prices.date)

data_store = pd.HDFStore("DJUSTC Prices and Ratios.h5", complevel=9, complib='blosc')

for ticker in set(prices.ticker):
    data = prices[prices.ticker == ticker]
    years = set(data.date.apply(lambda x: x.year))
    for year in years:
        data_by_year = data[data.date.apply(lambda x: x.year)==year]
        
        augment = ratios[(ratios.ticker == ticker)][[str(year)]].iloc[:,0]
        if (augment.isnull().all()==True) and year == 2018:
            augment = ratios[(ratios.ticker == ticker)][["TTM"]].iloc[:,0]
        augment = pd.DataFrame(augment).transpose()
        for column in augment.columns:
            #break
            data_by_year[column]=augment[column].iloc[0]
        
        data_by_year.columns = data_by_year.columns.str.replace("^[0-9]. ","").str.replace(" ","_")
        print(ticker, year)
        data_store.append("Output", data_by_year ,min_itemsize={'ticker':5})
    #output = pd.DataFrame(prices.iloc[i].append(augment)).transpose()
    #output.to_hdf('DJUSTC Prices and Ratios.h5',"Output",append=True)
    #output = output.append(prices.iloc[i].append(augment),ignore_index=True) 
data_store.close()