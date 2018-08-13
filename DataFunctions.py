# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 18:42:25 2018

@author: YJ
"""

import os
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import datetime,time
import re
from datetime import datetime
import requests

def alpha_vantage_download(api):
    os.chdir("C:/Users/YJ/Documents/1) Learning/Udacity - Machine Learning/capstone/Udacity-Machine-Learning-Engineer-Capstone-Project/Data Raw")
    
    DJUSTC = pd.read_csv("TickerNamesDJUSTC.csv")
    tickers = list(DJUSTC.Symbol)
    ts = TimeSeries(key=api, output_format='pandas')
    output = pd.DataFrame()
    
    for ticker in tickers:
        data, meta_data = ts.get_daily_adjusted(symbol=ticker, outputsize='full')
        data['ticker'] = ticker
        output = output.append(data.iloc[-750:])
        print(ticker)
        time.sleep(30)
        
    output.to_csv("DJUSTC Prices.csv")

def morningstar_download(input_file="../TickerNamesDJUSTC.csv"):
    os.chdir("C:/Users/YJ/Documents/1) Learning/Udacity - Machine Learning/capstone/Udacity-Machine-Learning-Engineer-Capstone-Project/Data Raw/Morningstar Financials")
    DJUSTC = pd.read_csv(input_file)
    tickers = list(DJUSTC.Symbol)
    
    #url_part1 = "http://financials.morningstar.com/ajax/ReportProcess4CSV.html?t="
    #url_part2 = "&reportType=is&period=12&dataType=A&order=asc&columnYear=5&number=3"
    
    url_all = "http://financials.morningstar.com/ajax/exportKR2CSV.html?t="
    
    for ticker in tickers:
        url = url_all + ticker
        #r = requests.get(url, allow_redirects=True, headers=headers)
        r = requests.get(url, allow_redirects=True)
        while r.status_code!=200:
            r = requests.get(url, allow_redirects=True)
        open(ticker+'.csv', 'wb').write(r.content)
        if len(r.content)==0:
            print(ticker, len(r.content))
            
        time.sleep(10)

def morningstar_cleaning(output_file = "DJUSTC Key Ratios.csv"):
    os.chdir("C:/Users/YJ/Documents/1) Learning/Udacity - Machine Learning/capstone/Udacity-Machine-Learning-Engineer-Capstone-Project/Data Raw/Morningstar Financials")
    output = pd.DataFrame()
    regex = re.compile(",(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)")
    for dirpath, dirnames, filenames in os.walk("C:/Users/YJ/Documents/1) Learning/Udacity - Machine Learning/capstone/Udacity-Machine-Learning-Engineer-Capstone-Project/Data Raw/Morningstar Financials"):
        for f in filenames:
            fhand = open(f)
            mylist = []
            #i=0
            for line in fhand:
                list_to_append = re.split(regex,line)
    
                for i in range(len(list_to_append)):
                    list_to_append[i]=list_to_append[i].replace("\"", "").replace(",", "").replace("\n","")
                
                mylist.append(list_to_append)
                #i+=1
                #if i==4:
                    #break
            data=pd.DataFrame(mylist)
            mydata =  data[3:18]
            mydata.columns = data.iloc[2].apply(lambda x: x[:4])
            mydata['ticker'] = f.replace(".csv","")
            output = output.append(mydata)
    
    output.to_csv("../"+output_file)
    
def data_merging_hdf():
    os.chdir("C:/Users/YJ/Documents/1) Learning/Udacity - Machine Learning/capstone/Udacity-Machine-Learning-Engineer-Capstone-Project/Data Raw")

    ratios = pd.read_csv("DJUSTC Key Ratios.csv")
    ratios.index = ratios[ratios.columns[1]]
    ratios = ratios.drop(ratios.columns[[0,1]],axis=1)
    
    
    prices = pd.read_csv("DJUSTC Prices.csv")
    prices.date = prices.date.apply(lambda x: datetime.strptime(x, "%d/%m/%Y"))
    prices.date = pd.to_datetime(prices.date)
    
    data_store = pd.HDFStore("DJUSTC Prices and Ratios.h5", complevel=9, complib='blosc')
    
    for ticker in set(prices.ticker):
        data = prices[prices.ticker == ticker]
        years = set(data.date.apply(lambda x: x.year))
        for year in years:
            data_by_year = data.loc[data.date.apply(lambda x: x.year)==year]
            
            augment = ratios[(ratios.ticker == ticker)][[str(year)]].iloc[:,0]
            if (augment.isnull().all()==True) and (year == 2018 or year==2017):
                augment = ratios[(ratios.ticker == ticker)][["TTM"]].iloc[:,0]
            augment = pd.DataFrame(augment).transpose()
            for column in augment.columns:
                #break
                data_by_year[column]=augment[column][0]
            
            data_by_year.columns = data_by_year.columns.str.replace("^[0-9]. ","").str.replace(" ","_")
            print(ticker, year)
            data_store.append("Output", data_by_year ,min_itemsize={'ticker':5})
        #output = pd.DataFrame(prices.iloc[i].append(augment)).transpose()
        #output.to_hdf('DJUSTC Prices and Ratios.h5',"Output",append=True)
        #output = output.append(prices.iloc[i].append(augment),ignore_index=True) 
    data_store.close()