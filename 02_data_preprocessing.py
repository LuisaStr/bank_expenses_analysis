# now that the pdf is stored within seperate columns in a data frame, 
# the data has to be pre-processed in order to be able to analyze it afterwards


# 1: change the date format to a valid date format
# 2: change the number format of monetary values


import pandas as pd
import re
from datetime import datetime
import numpy as np

#1.1: create a dict for the month to number transformation
month_to_number_dict = {
    "ene": "01",
    "feb": "02",
    "mar": "03",
    "abr": "04",
    "may": "05",
    "jun": "06",
    "jul": "07",
    "ago": "08",
    "sept": "09",
    "oct": "10",
    "nov": "11",
    "dic": "12"
}

#1.2: create a function that converts the date to dateformat
def convert_to_dateformat(date:str):

    month_re = re.compile(r'\d{2}\s(\w+)\s\d{4}')
    month_name = month_re.match(date).group(1) #store the fraction of regex in month_name
    month_number = month_to_number_dict[month_name] #apply the fraction of regex to the dict 

    string_date = re.sub(month_name, month_number, date) #safe the date with the replaced month format 

    return datetime.strptime(string_date, '%d %m %Y').date() #.date() in order not to have time

df = pd.read_excel("full_bank_data.xlsx")
df["date"] = df["date"].map(lambda date: convert_to_dateformat(date)) #safe a new column (with the same name)

# control if the format is correct now:
print(df.dtypes)
df.date[0]

#1.3: create a new column: "month"
df["month"] = df["date"].map(lambda x: x.month)


#2: transform the amount columns into floats
#2.1: in python, an object can only be transfored into float if it has no ',' or other special caracters
df["quantity"] = df["quantity"].replace('[€]', '', regex=True)
df["quantity"] = df["quantity"].replace('[−]', '-', regex=True)
df["quantity"] = df["quantity"].replace('[.]', '', regex=True)
df["quantity"] = df["quantity"].replace('[,]', '.', regex=True)


df["saldo"] = df["saldo"].replace('[€]', '', regex=True)
df["saldo"] = df["saldo"].replace('[.]', '', regex=True)
df["saldo"] = df["saldo"].replace('[,]', '.', regex=True)

df["quantity"] = df["quantity"].astype(float)
df["saldo"] = df["saldo"].astype(float)

print(df)
print(df.dtypes)

#3: store df to excel file
df.to_excel("bank_data_clean.xlsx", index=False)


