# Description : Stock Market Dashboard to show some Exploratory Data Analysis.

import streamlit as st
import pandas as pd
from datetime import date
import requests

import yfinance as yf
from plotly import graph_objs as go
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
import datetime

# @st.cache
def load_data(ticker, start, end):
    data = yf.download(ticker, start, end)
    data.reset_index(inplace=True)
    return data

def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x = data.Date, y = data.Open, name = 'Stock Open'))
    fig.add_trace(go.Scatter(x = data.Date, y = data.Close, name = 'Stock Close'))
    fig.layout.update(title_text = 'Time Series Data', xaxis_rangeslider_visible = True)
    st.plotly_chart(fig)

def get_input():
    start_date = st.sidebar.date_input('Start Date', datetime.date(2019, 7, 6))
    end_date = pd.to_datetime(st.sidebar.date_input('End Date', datetime.date(2021, 7, 6)))
    stock_ticker = st.sidebar.text_input('Ticker Symbol', 'AAPL')
    return start_date, end_date, stock_ticker

st.title("Stock Market Web Applcation")

st.sidebar.header("User Input")

start_date, end_date, selected_stocks = get_input()
data_load_state = st.text("Load Data")
data = load_data(selected_stocks, start_date, end_date)
data_load_state.text("Loading Data... Done!")

st.subheader('Raw Data')
st.write(data.head())

plot_raw_data()
st.line_chart(data.Close)
st.line_chart(data.Volume)


# Display company name
company = yf.Ticker(selected_stocks)
company_name = company.info['longName']
st.write(company_name)