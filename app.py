# Description : Stock Market Dashboard to show some Exploratory Data Analysis.

import streamlit as st
import pandas as pd
from datetime import date
import requests

import yfinance as yf
from plotly import graph_objs as go
import datetime
from custom_functions import *

st.title("Stock Market Web Applcation")

st.sidebar.header("User Input")

start_date, end_date, selected_stocks = get_input()
data_load_state = st.text("Load Data")
data = load_data(selected_stocks, start_date, end_date)
data_load_state.text("Loading Data... Done!")

st.subheader('Raw Data')
st.write(data.head())

data = generate_MACD(data)
data = generate_RSI(data)

data['SMA'] = generate_SMA(data)
data['EMA'] = generate_EMA(data)

plot_raw_data(data)

fig = go.Figure()
fig.add_trace(go.Scatter(x = data.Date, y = data.MACD, name = 'Moving Average Divergence/Convergence'))
fig.add_trace(go.Scatter(x = data.Date, y = data.Signal_Line, name = 'Signal Line'))
fig.layout.update(title_text = 'Moving Average Divergence/Convergence and Signal Line', xaxis_rangeslider_visible = True)
st.plotly_chart(fig)

st.line_chart(data.RSI)
st.line_chart(data.Volume)


# Display company name
company = yf.Ticker(selected_stocks)
company_name = company.info['longName']
st.write(company_name)