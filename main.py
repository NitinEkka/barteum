import datetime
import yfinance as yf
import csv
import pandas as pd
import numpy as np

# GET LAST 30 WEEKDAYS
def get_last_30_weekdays_data(current_date):
    weekdays = []
    days_count = 0

    while len(weekdays) < 30:
        previous_date = current_date - datetime.timedelta(days=days_count)
        if previous_date.weekday() < 5: 
            weekdays.append(previous_date)
        days_count += 1

    weekday_data = []

    for weekday in weekdays:
        weekday_data.append(weekday)

    return weekday_data


current_date = datetime.datetime.now() 
last_30_weekdays_data = get_last_30_weekdays_data(current_date)
new_list = []
new_list.append(last_30_weekdays_data)
symbol = "AAPL" 
start_date = new_list[0][-1]
end_date = new_list[0][0]

# DOWNLOAD DATA FROM YAHOO FINANCE FROM RESPECTIVE DATES AND ADD DIFFERENCE COLUMN
data = yf.download(symbol, start=start_date, end=end_date)
data.to_csv("candlestick_data.csv", index=True)
filename = "candlestick_data.csv"  
data = pd.read_csv(filename)
data['Difference'] = data['High'] - data['Low']
data.to_csv(filename, index=False)

# GET THE LAST 30TH DATE DATA FOR COMPARISION
def get_first_element(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader) 
        for row in reader:
            return row[0]

csv_file = 'candlestick_data.csv'
first_element = get_first_element(csv_file)
result = data.loc[data['Date'] == first_element, 'Difference'].iloc[0] # LAST 30TH DATE's DIFFERENCE VALUE

# CREATE THE COMPARISION AND PERCENTILE COLUMN
data["30th/current"] = data['Difference'] - result
data.to_csv(filename, index=False)
percentiles = np.percentile(data['Difference'], range(101))
data['Percentile'] = pd.Series(np.searchsorted(percentiles, data['Difference']) / 100)

print(data)
data.to_csv(filename, index=False)
    
