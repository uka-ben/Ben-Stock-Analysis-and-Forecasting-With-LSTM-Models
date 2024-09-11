import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import datetime
import helper
import preprocessing_model
from sklearn.metrics import mean_absolute_error , mean_squared_error , mean_absolute_percentage_error , r2_score

def Forecasting(stock_symbol):
    clean  = stock_symbol.replace(".JK" , " ")
    st.title(':blue[Stock Price Prediction Using LSTM]')

    st.divider()

    st.markdown("""
       **This application provides a robust tool for forecasting future stock prices using advanced Long Short-Term Memory (LSTM) models.** 

        the application will utilize the LSTM model to analyze historical price data and generate forecasts for the upcoming month. The LSTM model is particularly effective at capturing complex patterns and trends within time series data, providing valuable insights into potential future price movements.

    """)

    st.subheader(f"You have selected: {clean}")

    st.divider()


    col1 , col2 = st.columns(2)
    with col1 : 
        start = st.date_input("Start-Date : " , value=pd.to_datetime('2023-01-01'))
    with col2 : 
        end = st.date_input("Start-Date : " , value=pd.to_datetime(datetime.date.today()))
    
    forecast = st.slider(label="How many days would you like to forecast ? ", min_value=1 , max_value=30, step=1)

    data = yf.download(stock_symbol , start=start , end=end)


    if st.button('Fit Model and Forecast') :

        datasets = preprocessing_model.make_datasets(data=data)

        scaled_data = preprocessing_model.scale_data(datasets=datasets)

        train_len =  preprocessing_model.split_num(datasets=datasets) 

        x_train , y_train =  preprocessing_model.preprocessing( scaled_data=scaled_data["scaled_data"] , train_len=train_len)

        model =  preprocessing_model.modelling(x_train , y_train)

        prediction =  preprocessing_model.test_data(model=model , datasets=datasets , scaled_data=scaled_data['scaled_data'] , train_len=train_len , scaler=scaled_data['scaler'])

        forecast_value =  preprocessing_model.meramal(scaled_data=scaled_data['scaled_data'] , scaler=scaled_data['scaler'] , model=model , days=forecast)

        business_days = pd.bdate_range(start=end, periods=forecast)

        forecast_final = pd.DataFrame({"Date" : business_days , "forecast" : forecast_value}).set_index("Date")

        train = data[:train_len]
        test = data[train_len:]
        test['prediction'] = prediction

        with st.expander("Stock Data") : 
                
            with st.container(height=400) :
                st.table(data) 
        
        with st.expander("prediction plot and metrics"):

            st.title("Prediction Plot")
            st.plotly_chart(helper.predictions_plot(train , test , ))

            st.title("metrics")
            st.divider()
            col1,col2,col3 = st.columns(3)
            with col1 : 
                st.subheader("Root Mean Squared Error :")
                st.subheader(f":blue[{np.sqrt(mean_squared_error(test.Close , test.prediction)):.4f}]")
            with col2 : 
                st.subheader("Mean Absolute Error :")
                st.subheader(f":blue[{mean_absolute_error(test.Close , test.prediction):.4f}]")
            with col3 : 
                st.subheader("Mean Squared Error :")
                st.subheader(f":blue[{mean_squared_error(test.Close , test.prediction):.4f}]")
            
            col1,col2,col3 = st.columns([2,3,1])
            with col1 : 
                st.subheader("R2 - Squared :")
                st.subheader(f":blue[{(r2_score(test.Close , test.prediction)):.4f}]")
            with col2 : 
                st.subheader("Mean Absolute Percentage Error :")
                st.subheader(f":blue[{mean_absolute_percentage_error(test.Close , test.prediction):.4f}]")
                                         

            st.divider()

        with st.expander("Prediction Data"):
            with st.container(height=400) :
                st.table(test[['Close' , 'prediction']])      


        with st.expander("Forecasting") :
            st.table(forecast_final)  
            st.plotly_chart(helper.line_plot(data=forecast_final , color='blue' , column='forecast'))    


        



            

 
