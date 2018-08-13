# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 18:53:03 2018

@author: YJ
"""
import os
os.chdir("C:/Users/YJ/Documents/1) Learning/Udacity - Machine Learning/capstone/Submission")
import DataFunctions

api = input("Please inset the api key: ")
DataFunctions.alpha_vantage_download(api)
DataFunctions.morningstar_download()
DataFunctions.morningstar_cleaning()
DataFunctions.data_merging_hdf()