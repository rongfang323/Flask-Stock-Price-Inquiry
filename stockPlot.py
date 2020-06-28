from flask import Flask, render_template, request, redirect
import requests, bokeh
from bokeh.plotting import figure, output_file, show
import pandas as pd
from datetime import date, timedelta

symbol = 'BA'
# Define the address for request
apikey = 'WT5BYLL3700T2HN8'
request = 'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=' + symbol + '&apikey=' + apikey

response = requests.get(request)
         # response2 = json.dumps(response.content)

df = pd.read_json(response.content)
# print(df)

# eliminate the meta attribute
df = df[df['Monthly Time Series'].isnull() == False]



# read the date and time
datetime = pd.Series(df.index)
datetime = pd.to_datetime(datetime[:])

# Normalize the data frame of the stock prince
df = pd.json_normalize(df['Monthly Time Series'])

# combine datatime with df
stockSerie = pd.concat([datetime, df], axis=1)
stockSerie.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
stockSerie['Date'] = pd.to_datetime(stockSerie['Date']).dt.date

# find today's date and the date of a year ago
today = date.today()
yearAgo = timedelta(days=365)

# extract yearly record
stockSerieYear = stockSerie[stockSerie['Date'] >= today - yearAgo]
print(stockSerieYear)

# ploting the price vs. time
output_file('my_first_graph.html')
p = figure(x_axis_type="datetime")
p.line(stockSerieYear['Date'], stockSerieYear['Close'], line_width=2, color='red')
show(p)







