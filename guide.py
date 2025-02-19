import streamlit as st


def Forecast():

    st.title("Stock Forecasting Page (LSTM)")

    st.header("Overview")
    st.write("forecast stock prices using an LSTM (Long Short-Term Memory) model. LSTM is a type of recurrent neural network (RNN) that is particularly well-suited for time series data due to its ability to remember patterns over time. The model is trained on historical stock price data to predict future prices based on user-defined parameters.")

    st.header("Pre-set Parameters")
    st.markdown("The LSTM model on this page comes with pre-configured parameters for ease of use. Users do not need to adjust these, as they have been optimized based on historical data. The pre-set parameters include:")

    st.markdown("- Number of epochs: 1 ")
    st.markdown("- Batch size: 1 ")
    st.markdown("- Sequence length: 60 ")
    st.markdown("- Learning rate: 0.0001 ")
    st.markdown("- Optimizer: Adam ")
    st.markdown("- Activition Function : linear")
    st.markdown("- Scaler : MinMaxScaler")
    st.markdown("- Loss Function : mean_squared_error")
    st.markdown ("- Train size : 80 %")


    st.markdown("""
    ## Stock Forecasting Guide

    This page helps you forecast stock prices by selecting a date range and specifying how many days ahead you want predictions. The model automatically splits the data, trains an LSTM model, and generates forecasts.

    ### How It Works:

    1. **Select a Date Range**  
       - Use the date picker to define the stock data period for analysis.  
       - The model will split the data into training and testing sets.  

    2. **Set Forecasting Days**  
       - Enter the number of future days to predict.  

    3. **Run the Forecast**  
       - Click the "Forecast" button to train the model and generate predictions.  

    4. **View Results**  
       - A line graph will display actual vs. predicted prices.  
       - Metrics like MSE, RMSE, and MAE will assess model accuracy.  
""")
