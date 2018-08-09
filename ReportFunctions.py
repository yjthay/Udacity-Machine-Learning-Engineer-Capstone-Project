# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 19:25:40 2018

@author: YJ
"""
import os
import pandas as pd
import alpha_vantage as av
from alpha_vantage.timeseries import TimeSeries
import numpy as np
import datetime,time
import re
from datetime import datetime
import matplotlib
from matplotlib import pyplot as plt

def returns_x_days(adjusted_close, days = 30):
    dates = adjusted_close.index.sort_values(ascending=True)
    output = pd.DataFrame()
    for start_date,end_date in zip(dates[:-days],dates[days:]):
        start_level = adjusted_close.loc[start_date]
        end_level = adjusted_close.loc[end_date]
        returns = end_level-start_level
        binary_returns = returns.apply(lambda x: 1 if x>0 else 0)
        output[end_date]=binary_returns
    output.index = pd.MultiIndex.from_tuples([("returns_x_days",index) for index in output.index],names = ['data_types','tickers'])
    output = output.transpose()
    output.index.name = "date"
    
    return output

def describe_axis(pivot):
    print("We have ",len(pivot.columns.names)," levels in columns")
    print("The levels are ",pivot.columns.names)
    for level in pivot.columns.names:
        print("\n There are ",len(pivot.columns.get_level_values(level).unique()), " unique values in ", level)
        print("\n ",level, " has the following unique values: \n", pivot.columns.get_level_values(level).unique())

    print("**************************************************************************************")

    print("We have ",len(pivot.index.names)," level in index")
    print("The levels are ",pivot.index.names)
    for level in pivot.index.names:
        print("\n There are ",len(pivot.index.get_level_values(level).unique()), " unique values in ", level)
        print("\n ",level, " has the following unique values: \n", pivot.index.get_level_values(level).unique())

def plot_before_after(adjusted_pivot, pivot, indices_to_adjust, tickers):
    changes_made = len(tickers) * len(indices_to_adjust)
    fig, axes = plt.subplots(nrows=changes_made, ncols=2,figsize=(15,changes_made*4))
    plot_number=0
    for index in indices_to_adjust:
        for ticker in tickers:
            (adjusted_pivot.xs(index, axis=1, level=0).xs(ticker, axis=1)).plot(ax=axes[plot_number,0],
                                                                            title = ticker + "_" + index.upper() + "_After").axis('off')
            (pivot.xs(index, axis=1, level=0).xs(ticker, axis=1)).plot(ax=axes[plot_number,1],
                                                                    title = ticker + "_" + index.upper() + "_Before").axis('off')
            plot_number+=1

def data_for_modelling(X_train,y_train,ticker=slice(None),days = 30):
    X_train_unstack,y_train_unstack = list(),list()
    #X_test_unstack,y_test_unstack = pd.DataFrame(),pd.DataFrame()
    for start,end in zip(X_train.index[:-days],X_train.index[days:]):
        X_train_unstack.append(X_train.loc[start:end,(slice(None),ticker)].unstack().transpose().values)
        y_train_unstack.append(y_train.loc[end,ticker])
    return np.array(X_train_unstack), np.array(y_train_unstack)

def check_missing(pivot):
    total = pivot.isnull().sum().sort_values(ascending = False)
    percent = (pivot.isnull().sum()/pivot.isnull().count()*100).sort_values(ascending = False)
    missing_data  = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
    return missing_data[missing_data['Total']>0]