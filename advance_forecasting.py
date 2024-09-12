import streamlit as st
import pandas as pd
import preprocessing_model
import yfinance as yf
import datetime
import helper
import numpy as np
from sklearn.metrics import mean_absolute_error , mean_squared_error , mean_absolute_percentage_error , r2_score



def Forecasting(stock):

    cleaned_stock = stock.replace(".JK" , " ")

    st.title(':blue[Customizable LSTM for Stock Price Prediction]')
    st.divider()
    st.markdown("""
        **This application offers a powerful tool for forecasting future stock prices using advanced Long Short-Term Memory (LSTM) models.** 

         In this section, users can customize the LSTM model parameters to optimize stock price predictions. You can adjust the number of epochs, learning rate, and other parameters, allowing you to explore different settings and find the most effective combination for the data being analyzed.
    """)

    st.subheader(f"You Have Selected : {cleaned_stock}")
    st.divider()

    col1 , col2 = st.columns(2)
    with col1 : 
        start = st.date_input("Start-Date : " , value=pd.to_datetime('2023-01-01'))
    with col2 : 
        end = st.date_input("Start-Date : " , value=pd.to_datetime(datetime.date.today()))
    
    forecast = st.slider(label="How many days would you like to forecast ? ", min_value=1 , max_value=30, step=1)

    data = yf.download(stock , start=start , end=end)

    with st.container(border=True):
        st.title("Customize Your LSTM Model : ")

        train_len = st.select_slider(label="train size" ,options=[f"{i}%" for i in range(10, 101, 10)])
        activation = st.selectbox( label='Activation Function for Dense Layers',options=['relu', 'sigmoid', 'tanh','linear'])

        col1 , col2 , col3 = st.columns(3)

        with col1 :
            learning_rate = st.selectbox(label='Learning Rate', options=[0.1 ,0.01 , 0.001, 0.0001])
            window = st.selectbox(label="Window Size" , options=[20,40,60,80,100,120,140,180])
        with col2 :
            optimizer = st.selectbox(label="Optimizer",options=["Adam", "SGD", "RMSprop", "Adagrad", "Adadelta"])
            epochs = st.selectbox(label="Epochs",options=[1,3,5,10, 20, 30, 40, 50, 100, 200])
        with col3  :
            loss_function = st.selectbox(label="Loss Function",options=["mean_squared_error","mean_absolute_error", "huber_loss","mean_absolute_percentage_error"])
            batch_size = st.selectbox(label="Batch Size",options=[1,16, 32, 64, 128, 256])
        
        scaler = st.selectbox(label="Scaler",options=["StandardScaler", "MinMaxScaler", "RobustScaler"])


    if st.button("Apply Model & Forecast Data") :

        datasets = preprocessing_model.make_datasets(data=data)

        scaled_data = preprocessing_model.scale_data(datasets=datasets , scale=scaler)

        train_len =  preprocessing_model.split_num(datasets=datasets , size=int(train_len.replace("%", "")) / 100) 

        x_train , y_train =  preprocessing_model.preprocessing( scaled_data=scaled_data["scaled_data"] , train_len=train_len , window=window)

        model =  preprocessing_model.modelling(x_train , y_train , batch=batch_size , epoch=epochs , window=window , learning_rate=learning_rate , optimize=optimizer , loss_function=loss_function, function_activation=activation)

        prediction =  preprocessing_model.test_data(model=model , datasets=datasets , scaled_data=scaled_data['scaled_data'] , train_len=train_len , scaler=scaled_data['scaler'])

        forecast_value =  preprocessing_model.meramal(scaled_data=scaled_data['scaled_data'] , scaler=scaled_data['scaler'] , model=model , days=forecast , window=window)

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


        



            

 






        

            


