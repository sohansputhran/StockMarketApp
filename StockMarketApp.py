# Description: This is a stock market dashboard to show some charts and data on some stock

import streamlit as st
import pandas as pd
from PIL import Image

import yfinance as yf

# Add a title
st.write("""
# Stock Market Web Application
**Visually** show the data on a stock! Date range from 2015-06-01 to 2021-06-25
""")

# image = Image.open(path)
# st.image(image, use_column_width = True)

# Create a sidebar header
st.sidebar.header("User Input")

# Create a function to get the user input
def get_input():
    start_date = st.sidebar.text_input('Start Date', '2015-06-01')
    end_date = st.sidebar.text_input('Start Date', '2021-06-25')
    stock_symbol = st.sidebar.text_input('Stock Symbol', 'MSFT')
    return start_date, end_date, stock_symbol

# Create a function to get the company name
def get_company_name(symbol):
    if symbol == 'MSFT':
        return 'Microsoft'
    elif symbol == 'GOOG':
        return 'Google'
    elif symbol == 'TSLA':
        return 'Tesla'
    else:
        'None'

# Create a function to get the proper company data and the proper timeframe from the user
def get_data(symbol, start, end):
    
    # Load the data
    if symbol.upper() == 'MSFT':
        MSFT = yf.Ticker('MSFT')
        df = MSFT.history(period='1d', start= start, end= end)

    elif symbol.upper() == 'GOOG':
        GOOG = yf.Ticker('GOOG')
        df = GOOG.history(period='1d', start= start, end= end)

    elif symbol.upper() == 'TSLA':
        TSLA = yf.Ticker('TSLA')
        df = TSLA.history(period='1d', start= start, end= end)

    else:
        df = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits'])

    # Create a column for Date from the datetime index to regular index
    df.reset_index(inplace= True)

    # Get the date range
    start = pd.to_datetime(start)
    end = pd.to_datetime(end)

    # Set the start and end index rows both to 0
    start_row = 0
    end_row = 0

    # Start the date from the top of the data set and go down to see 
    # if the users start date is less than or equal to the date in the dataset
    for i in range(len(df)):
        if start <= pd.to_datetime(df['Date'][i]):
            start_row = i
            break

    # Start from the bottom of the dataset and go up to see 
    # if the users end date is greater than or equal to the date in the dataset
    for j in range(len(df)):
        if end >= pd.to_datetime(df['Date'][len(df) - 1 - j]):
            end_row = len(df) - 1 - j
            break

    # Set the index to be date
    df.set_index(pd.DatetimeIndex(df['Date'].values), inplace=True)

    return df.iloc[start_row : end_row + 1, :]

#Get the users input
start, end, symbol = get_input()

# Get the data
df = get_data(symbol, start, end)

#Get the company name
company_name = get_company_name(symbol.upper())

#Display the close price
st.header(company_name + ' Close Price\n')
st.line_chart(df['Close'])

#Display the volume
st.header(company_name + ' Volume\n')
st.line_chart(df['Volume'])

# Get statistics on the data
st.header('Data Statistics')
st.write(df.describe())