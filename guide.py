import streamlit as st


def Forecast():

    st.title("Stock Forecasting Page (LSTM)")

    st.header("Overview")
    st.write("This page provides users with the ability to forecast stock prices using an LSTM (Long Short-Term Memory) model. LSTM is a type of recurrent neural network (RNN) that is particularly well-suited for time series data due to its ability to remember patterns over time. The model is trained on historical stock price data to predict future prices based on user-defined parameters.")

    st.header("Pre-set Parameters")
    st.markdown("he LSTM model on this page comes with pre-configured parameters for ease of use. Users do not need to adjust these, as they have been optimized based on historical data. The pre-set parameters include:")

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
    ## How to Use the Stock Forecasting Page

    This page allows users to forecast stock prices by selecting a custom date range and choosing how many days they want to forecast into the future. The model will automatically split the data into training and testing sets, then train the LSTM model to predict the next days' prices.

    ### Steps:

    1. **Select Date Range**: 
    - Use the date picker to select the start and end dates of the stock data you want to use for the forecast. The selected range will be automatically divided into training and testing sets.
    - The training data will include all data before the final selected date, and the test data will include the last portion of data.

    2. **Choose Forecasting Days**:
    - Input how many days ahead you want to forecast. This number determines the length of the prediction, starting from the end of the test data.

    3. **Click the Forecast Button**:
    - Once you have selected the date range and the number of days to forecast, click the button to start the model. The LSTM model will automatically train on the selected data and provide a forecast for the specified number of days.

    4. **View Results**:
    - The forecast results will be displayed in a line graph comparing the actual historical prices with the predicted future prices. Evaluation metrics such as MSE, RMSE, and MAE will also be shown to indicate the model’s performance.
    """)
