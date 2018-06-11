import pandas as pd
import os
import re

os.chdir("C:/Users/YJ/Documents/1) Learning/Udacity - Machine Learning/capstone/Submission/Morningstar Financials")
output = pd.DataFrame()
regex = re.compile(",(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)")
for dirpath, dirnames, filenames in os.walk("C:/Users/YJ/Documents/1) Learning/Udacity - Machine Learning/capstone/Submission/Morningstar Financials"):
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
        print(data.iloc[2].apply(lambda x: x[:4]))
        data=pd.DataFrame(mylist)
        mydata =  data[3:18]
        mydata.columns = data.iloc[2].apply(lambda x: x[:4])
        mydata['ticker'] = f.replace(".csv","")
        output = output.append(mydata)

output.to_csv("../DJUSTC Key Ratios.csv")
#https://stackoverflow.com/questions/18893390/splitting-on-comma-outside-quotes
#https://stackoverflow.com/questions/23205606/regex-to-remove-comma-between-double-quotes-notepad