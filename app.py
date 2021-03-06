import request as request
from flask import Flask, render_template, request, redirect, make_response
import requests, bokeh
from bokeh.plotting import figure, output_file, show, output_notebook
from bokeh.embed import components
import pandas as pd
from datetime import date, timedelta




app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('layout.html')

@app.route('/plotrender', methods=['POST'])
def my_form_post():
    variable = request.form['variable']
    symbol = variable

    # Define the address for request
    apikey = 'WT5BYLL3700T2HN8'
    request1 = 'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=' + symbol + '&apikey=' + apikey

    response = requests.get(request1)


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

    # ploting the price vs. time
    titleStr = 'Monthly Stock Price of ' + variable + ' for the recent 12 months'

    #output_file('my_first_graph.html', title=variable)

    p = figure(x_axis_type="datetime", title = titleStr )
    p.line(stockSerieYear['Date'], stockSerieYear['Close'], line_width=2, color='red')
    script, div = components(p)
    print(script)
    print(div)

    return  render_template('plotrender.html', div=div, script = script)




if __name__ == '__main__':
    app.run(port=33509, debug=True)
