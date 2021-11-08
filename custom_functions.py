import streamlit as st
import pandas as pd
from datetime import date
import requests

import yfinance as yf
from plotly import graph_objs as go

def get_input(default_start_date, default_end_date):
    start_date = st.sidebar.date_input('Start Date', default_start_date)
    end_date = pd.to_datetime(st.sidebar.date_input('End Date', default_end_date))
    stock_ticker = st.sidebar.text_input('Ticker Symbol', 'AAPL')
    return start_date, end_date, stock_ticker

def load_data(ticker, start, end):
    data = yf.download(ticker, start, end)
    data.reset_index(inplace=True)
    data = data.set_index(pd.DatetimeIndex(data['Date']).values)
    return data

# Simple Moving Average (SMA)
def generate_SMA(data, period = 20, column = 'Close'):
    return data[column].rolling(window = period).mean()

# Exponential Moving Average (EMA)
def generate_EMA(data, period = 20, column = 'Close'):
    return data[column].ewm(span = period, adjust = False).mean()

# Moving Average Convergence / Divergence (MACD)
def generate_MACD(data, period_long = 26, period_short = 12, period_signal = 9, column = 'Close'):
    
    # Short term EMA
    short_EMA = generate_EMA(data, period_short, column)
    # Long term EMA
    long_EMA = generate_EMA(data, period_long, column)
    data['MACD'] = short_EMA - long_EMA
    data['Signal_Line'] = generate_EMA(data, period_signal, "MACD")
    return data

# Relative Strength Index (RSI) 
def generate_RSI(data, period = 14, column = 'Close'):
    delta = data[column].diff(1)
    delta = delta[1:]
    
    up = delta.copy()
    down = delta.copy()

    up[ up < 0] = 0
    down[ down > 0] = 0

    data['up'] = up
    data['down'] = down

    AVG_gain = generate_SMA(data, period, 'up')
    AVG_loss = abs(generate_SMA(data, period, 'down'))

    RSI = 100.0 - (100.0 / (1.0 + (AVG_gain / AVG_loss)))
    data['RSI'] = RSI

    return data

def plot_raw_data(data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x = data.Date, y = data.SMA, name = 'Simple Moving Average'))
    fig.add_trace(go.Scatter(x = data.Date, y = data.EMA, name = 'Exponential Moving Average'))
    fig.add_trace(go.Scatter(x = data.Date, y = data.Close, name = 'Stock Close'))
    fig.layout.update(title_text = 'Time Series Data', xaxis_rangeslider_visible = True)
    st.plotly_chart(fig)