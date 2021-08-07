import streamlit as st

from datetime import date

import yfinance as yf
from plotly import graph_objs as go

START = '2018-01-01'
TODAY = date.today().strftime("%Y-%m-%d")

st.title("Stock Prediction App")

stocks = ("AAPL", 'GOOG', 'MSFT', 'GME')
selected_stocks = st.selectbox("Select dataset for prediction", stocks)

n_years = st.slider("Years of Prediction:", 1, 4)
period = 365 * n_years

@st.cache
def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data

data_load_state = st.text("Load Data")
data = load_data(selected_stocks)
data_load_state.text("Loading Data... Done!")

st.subheader('Raw Data')
st.write(data.head())

def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x = data.Date, y = data.Open, name = 'Stock Open'))
    fig.add_trace(go.Scatter(x = data.Date, y = data.Close, name = 'Stock Close'))
    fig.layout.update(title_text = 'Time Series Data', xaxis_rangeslider_visible = True)
    st.plotly_chart(fig)

plot_raw_data()