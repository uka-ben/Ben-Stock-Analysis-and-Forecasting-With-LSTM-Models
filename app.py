import streamlit as st
import analysis_one
import analysis_multiple
import forecasting
import advance_forecasting
import pandas as pd
import guide

st.set_page_config(layout="wide")

ticker_list = pd.read_csv("Ticker_list.csv")


st.image("picture.png", caption="My Name Is Benjamin Uka.",use_column_width=True)
section = st.radio(
    "**Select Section:**", 
    options=["📊 In-Depth Analysis","🔮 Future Trends Forecast", "⚙️ Customize LSTM Parameters","📈 Stock Symbols"])
st.divider()

ticker= ticker_list['Ticker'].values
ticker_map = {ticker: ticker + '.JK' for ticker in ticker}
display_names = list(ticker_map.keys())

selected_display_name = st.selectbox('Pick a Stock for Analysis & Forecast',  options=display_names , index=1) 
stock_symbol = ticker_map[selected_display_name]




if section == "📊 In-Depth Analysis" : 

    tab1, tab2 = st.tabs(["Single Stock Analysis", "Multiple Stock Analysis"])

    with tab1 :

        analysis_one.Analysis_stock_data(stock_symbol=stock_symbol)
    
    with tab2 : 
         
      selected_display_names = st.multiselect('Pick a Stock for Multiple Analysis', options=display_names , max_selections=4 , default=display_names[:2])

      selected_symbols = [ticker_map[name] for name in selected_display_names]

      analysis_multiple.multiply_alalysis(selected_symbols)

elif section == "🔮 Future Trends Forecast":

    tab1 , tab2 = st.tabs(["Forecast" , "Documentation"])

    with tab1 : 
        forecasting.Forecasting(stock_symbol = stock_symbol)
    with tab2 : 
        guide.Forecast()

elif section == '⚙️ Customize LSTM Parameters':
    advance_forecasting.Forecasting(stock=stock_symbol)
elif section == '📈 Stock Symbols' :

    st.title(":red[Indonesia Stock]")

    search = st.text_input("Search : ")
    if st.button("Search"):
        if len(ticker_list[ticker_list['Ticker'] == search.upper()]) > 0 : 
            st.table(ticker_list[ticker_list['Ticker'] == search.upper()])
        elif len(ticker_list[ticker_list['Company Name'] == search]) > 0 : 
            st.table(ticker_list[ticker_list['Company Name'] == search])
        else :
            st.error("stock not available here.")

    st.table(ticker_list)
else : 
    st.title(":blue[select section]")








