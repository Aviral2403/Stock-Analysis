import numpy as np
import streamlit as st
import yfinance as yf
import pandas as pd
import pickle
import plotly.graph_objs as go
import datetime
pipe=pickle.load(open('pipe.pkl','rb'))
stock=pickle.load(open('stock.pkl','rb'))
# Streamlit App Header
st.title('Stock Analysis')
data = {
    'Company Name': ['ADANIPORTS', 'ASIANPAINT', 'AXISBANK', 'BAJAJ-AUTO', 'BAJAJ-AUTO-FINANCE', 'BAJAJ-FINANCE',
                     'BRITANNIA', 'CIPLA', 'HCL-TECHNOLOGIES', 'HDFC', 'HEROMOTOCO', 'ICICIBANK',
                      'INFOYS', 'ITC', 'NESTLEINDIA', 'NTPC', 'RELIANCE', 'TATAMOTORS',
                     'TATASTEEL', 'TCS',  'WIPRO'],
    'Stock Market Name': ['Adani Ports and Special Economic Zone Limited', 'Asian Paints Limited',
                          'Axis Bank Limited', 'Bajaj Auto Limited', 'Bajaj Auto Finance Limited',
                          'Bajaj Finance Limited',
                          'Britannia Industries Limited', 'Cipla Limited', 'HCL Technologies Limited',
                          'Housing Development Finance Corporation Limited',
                          'Hero MotoCorp Limited', 'ICICI Bank Limited',
                          'Infosys Limited', 'ITC Limited',
                          'Nestle India Limited', 'NTPC Limited', 'Reliance Industries Limited', 'Tata Motors Limited',
                          'Tata Steel Limited', 'Tata Consultancy Services Limited',
                            'Wipro Limited'],
    'Symbol':['ADANIPORTS.NS','ASIANPAINT.NS','AXISBANK.NS','BAJAJ-AUTO.NS','BAJFINANCE.NS','BAJAJFINSV.NS',
              'BRITANNIA.NS','CIPLA.NS','HCLTECH.NS','HDFCBANK.NS','HEROMOTOCO.NS','ICICIBANK.NS',
              'INFY','ITC.NS','NESTLEINDIA.NS','NTPC.NS','RELIANCE.NS','TATAMOTORS.NS','TATASTEEL.NS',
              'TCS.NS','WIPRO.NS']
}
df = pd.DataFrame(data)
st.subheader('List of Companies')
st.write(df)
st.markdown("Choose a stock from the given list to know about its current day analysis")
stock_symbol = st.selectbox('STOCK',stock['Symbol'].unique())
if stock_symbol:
    try:
        # Fetch stock data from Yahoo Finance for the past month
        stock_data = yf.Ticker(stock_symbol).history(period='2d')
        if not stock_data.empty:
            st.subheader( stock_symbol+ '  Details')
            st.write(f"Symbol: {stock_symbol.upper()}")
            current_price = stock_data['Close'].iloc[-1]
            st.write(f"Current Price: {current_price:.2f}")
            previous_close = stock_data['Close'].iloc[-2]
            st.write(f"Previous Close: {previous_close:.2f}")
            high = stock_data['High'].max()
            st.write(f"High: {high:.2f}")
            low = stock_data['Low'].min()
            vwap = (stock_data['Close'] * stock_data['Volume']).sum() / stock_data['Volume'].sum()
            st.write(f"VWAP: {vwap:.2f}")
            open_price = stock_data['Open'].iloc[0]
            st.write(f"Open: {open_price:.2f}")
            last = stock_data['Close'].iloc[-1]
            st.write(f"Last: {last:.2f}")
        else:
            st.warning("No data available for this stock symbol.")

    except Exception as e:
        st.error(f"An error occurred: {e}")

import yfinance as yf
import streamlit as st
import plotly.express as px
st.subheader("Historical Stock Price Analysis")
st.write("For a better graphical representation , select a week's gap minimum")
# Date range selection
start_date = st.date_input("Start Date:")
end_date = st.date_input("End Date:")
if start_date and end_date:
    if start_date <= end_date:
        try:
            # Fetch historical data for the selected date range
            stock_data = yf.download(stock_symbol, start=start_date, end=end_date)

            if not stock_data.empty:
                # Create a historical price chart
                fig = px.line(stock_data, x=stock_data.index, y='Close', title=f"{stock_symbol} Historical Prices")
                st.plotly_chart(fig)

                # Display data table
                st.write("Historical Data:")
                st.write(stock_data)

            else:
                st.warning("No data available for this stock symbol in the selected date range.")

        except yf.exceptions.YFinanceError as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Start Date should be before End Date.")


st.subheader("ESTIMATE PREDICTION OF STOCK PRICES")
st.markdown("Fill the given values to get a predicted price of the selected stock as per those values")
#creating dropdown boxex for different specifications
Stock = st.selectbox('Stock Name',stock['Symbol'].unique())
PrevClose = st.number_input('Previous CLose Price Of Stock')
Open = st.number_input('Enter Opening Value Of Stock On Current Day')
High = st.number_input('Highest Price Of Stock On Current Day')
Low = st.number_input('Lowest Buying/Selling Price Of Stock On Current day')
Last = st.number_input('Last Buying/Selling Price Of Stock On Current day')
VWAP = st.number_input('Volume-Weighted Average Price')

if st.button("Predict"):
    query = np.array([Stock , PrevClose , Open , High , Low , Last , VWAP])
    query = query.reshape(1,7)
    st.title("The predicted price is " + str(round(float(pipe.predict(query)[0]), 3)))

# Fetch today's date
today_date = datetime.date.today()

# Allow the user to select a date between 2008 and today
selected_date = st.date_input('Select a Date', min_value=datetime.date(2008, 1, 1), max_value=today_date, value=today_date)

# Map user-friendly time period names to Yahoo Finance API period strings
time_period_map = {
    '1 Day': '1d',
    '1 Week': '1wk',
    '1 Month': '1mo',
    '1 Year': '1y',
    '10 Years': '10y'
}

time_period = st.radio('Select Time Period:', ['1 Day','1 Week', '1 Month', '1 Year', '10 Years'])

if Stock and time_period:
    try:
        # Calculate the start and end dates based on the selected time period
        if time_period == '1 Day':
            start_date = selected_date
            end_date = selected_date + datetime.timedelta(days=1)
        elif time_period == '1 Week':
            start_date = selected_date
            end_date = selected_date + datetime.timedelta(weeks=1)
        elif time_period == '1 Month':
            start_date = selected_date
            end_date = selected_date + datetime.timedelta(days=30)
        elif time_period == '1 Year':
            start_date = selected_date
            end_date = selected_date + datetime.timedelta(days=365)
        elif time_period == '10 Years':
            start_date = selected_date
            end_date = selected_date + datetime.timedelta(days=3652)  # Approximately 10 years

        # Convert start_date and end_date to strings
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')

        # Fetch historical stock data for the selected stock and time period
        stock_data = yf.Ticker(Stock).history(start=start_date_str, end=end_date_str)

        if not stock_data.empty:
            st.write(f"Symbol: {Stock.upper()}")

            # Create a candlestick chart
            fig = go.Figure(data=[go.Candlestick(x=stock_data.index,
                                                open=stock_data['Open'],
                                                high=stock_data['High'],
                                                low=stock_data['Low'],
                                                close=stock_data['Close'])])

            # Customize the layout of the candlestick chart
            fig.update_layout(title=f'{Stock} Candlestick Chart ({time_period})',
                              xaxis_title='Date',
                              yaxis_title='Price',
                              xaxis_rangeslider_visible=True,
                              height=700,
                              width=1200)

            st.plotly_chart(fig)

        else:
            st.warning(f"No data available for this stock symbol ({Stock}) in the selected time period.")

    except Exception as e:
        st.error(f"An error occurred: {e}")

# Fetch today's date
today_date = datetime.date.today()

# Allow the user to select a date between 2008 and today
selected_date = st.date_input('Choose a Date', min_value=datetime.date(2008, 1, 1), max_value=today_date,
                              value=today_date)

# Convert the selected date to a string in the format 'YYYY-MM-DD'
selected_date_str = selected_date.strftime('%Y-%m-%d')

if Stock:
    try:
        # Fetch historical stock data for the selected stock and date
        stock_data = yf.Ticker(Stock).history(period='20y')

        # Filter data for the selected date
        selected_data = stock_data[stock_data.index.date == selected_date]

        if not selected_data.empty:
            # Display the stock details

            st.write(f"Symbol: {Stock.upper()}")

            # Date
            st.write(f"Selected Date: {selected_date_str}")

            # Open
            open_price = selected_data['Open'].iloc[0]
            st.write(f"Open: {open_price:.2f}")

            # High
            high = selected_data['High'].iloc[0]
            st.write(f"High: {high:.2f}")

            # Low
            low = selected_data['Low'].iloc[0]
            st.write(f"Low: {low:.2f}")

            # Close
            close_price = selected_data['Close'].iloc[0]
            st.write(f"Close: {close_price:.2f}")

            # Volume
            volume = selected_data['Volume'].iloc[0]
            st.write(f"Volume: {volume}")

        else:
            st.warning(f"No data available for the selected stock ({Stock}) on {selected_date_str}.")

    except Exception as e:
        st.error(f"An error occurred: {e}")


import yfinance as yf
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, timedelta  # Import the 'date' and 'timedelta' classes

# Streamlit app
st.title("Stock Performance Comparison")
st.write("For better analysis, do comparison for a week minimum")

# Input widgets for stock symbols
stock_symbol1 = st.selectbox('Stock 1 Name',stock['Symbol'].unique())
stock_symbol2 = st.selectbox('Stock 2 Name',stock['Symbol'].unique())
# Date range selection
today = date.today()
start_date = st.date_input("Select Start Date:", today - timedelta(days=2))
end_date = st.date_input("Select End Date:", today)

if start_date and end_date:
    if start_date < end_date and stock_symbol1 and stock_symbol2:
        try:
            # Fetch historical data for the selected date range for both stocks
            stock_data1 = yf.download(stock_symbol1, start=start_date, end=end_date)
            stock_data2 = yf.download(stock_symbol2, start=start_date, end=end_date)

            if not stock_data1.empty and not stock_data2.empty:
                # Create a line chart to compare the performance of both stocks
                fig = px.line(stock_data1, x=stock_data1.index, y='Close', title=f"{stock_symbol1} vs. {stock_symbol2} Performance")
                fig.add_scatter(x=stock_data2.index, y=stock_data2['Close'], mode='lines', name=stock_symbol2)

                st.plotly_chart(fig)

                # Display performance summary
                st.write("Performance Summary:")
                st.write(f"{stock_symbol1} - Start Price: {stock_data1['Close'][0]:.2f}, End Price: {stock_data1['Close'][-1]:.2f}")
                st.write(f"{stock_symbol2} - Start Price: {stock_data2['Close'][0]:.2f}, End Price: {stock_data2['Close'][-1]:.2f}")

            else:
                st.warning("No data available for one or both of the stock symbols in the selected date range.")

        except yf.exceptions.YFinanceError as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Start Date should be before End Date, and both stock symbols should be provided.")

