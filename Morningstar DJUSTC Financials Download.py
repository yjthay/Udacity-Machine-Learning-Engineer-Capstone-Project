#https://gist.github.com/hahnicity/45323026693cdde6a116
#https://gist.github.com/anonymous/c7d9c19cc67e03641966064d1518ed41

import os
import requests
import time
import pandas as pd

#user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36'
#headers = {'User-Agent': user_agent}


os.chdir("C:/Users/YJ/Documents/1) Learning/Udacity - Machine Learning/capstone/Submission")
DJUSTC = pd.read_csv("TickerNamesDJUSTC.csv")
tickers = list(DJUSTC.Symbol)

url_part1 = "http://financials.morningstar.com/ajax/ReportProcess4CSV.html?t="
url_part2 = "&reportType=is&period=12&dataType=A&order=asc&columnYear=5&number=3"

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
    