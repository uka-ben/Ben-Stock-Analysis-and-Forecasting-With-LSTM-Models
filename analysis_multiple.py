import streamlit as st
import pandas as pd
import helper
import time
import preprocessing
import datetime
import warnings
from scipy.stats import skew, kurtosis


def multiply_alalysis(stock):

    cleaned_stock = [symbol.replace(".JK", "") for symbol in stock]

    st.title(f":green[Multiple Stock Analysis]")

    st.markdown(
        """
                **Welcome to the Multi-Stock Analysis Dashboard!**

                Analyze multiple stocks simultaneously with powerful tools and insights. Select several stocks to compare performance across various metrics, including daily returns, cumulative returns, moving averages, and key financial ratios. 
                Gain a deeper understanding of stock trends and make informed decisions by exploring interactive visualizations and comprehensive analysis.

                **Start your multi-stock analysis now!**
                """
    )

    st.divider()
    if not stock:
        st.warning("**Please select at least two stock to proceed.**")
    else:
        st.subheader(f"**You have selected:** {', '.join(cleaned_stock)}")
    col1, col2 = st.columns(2)

    with col1:
        start = st.date_input("Start Date : ", value=pd.to_datetime("2023-01-01"))
    with col2:
        end = st.date_input("End Date : ", value=pd.to_datetime(datetime.date.today()))

    if "load" not in st.session_state:
        st.session_state.load = False

    if st.button("Fetch Data and Generate Analysis") or st.session_state.load:

        st.session_state.load = True

        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.050)
            progress_bar.progress(i + 1)

        data = preprocessing.download_multistock_data(
            list(stock), start_date=start, end_date=end
        )
        with st.expander("Display Stock Data"):

            with st.container(height=400):
                st.table(data)
            col1, col2 = st.columns([2, 1])
            with col1:
                st.subheader(f"Total Rows : {data.shape[0]}")
            with col2:
                st.subheader(f"Total Columns : {data.shape[1]}")

        with st.expander("Data Trends Overview"):

            st.title("Stock Price")
            st.plotly_chart(helper.plot_with_dropdown(data=data, tickers=stock))

            st.divider()
            col1, col2, col3 = st.columns(3)

            with col1:
                data_max = (
                    preprocessing.corr_data(data=data).tail(1).max().reset_index()
                )
                highest = data_max[data_max[0] == data_max[0].max()]
                st.subheader("Highest Price : ")
                st.subheader(
                    f":green[{highest['ticker'].values[0]} ({highest[0].values[0]:.2f})]"
                )

                data_vol = (
                    preprocessing.corr_data(data=data, columns="Volume")
                    .tail(1)
                    .max()
                    .reset_index()
                )
                vol = data_vol[data_vol[0] == data_vol[0].max()]
                st.subheader("Highest Volume  : ")
                st.subheader(
                    f":green[{vol['ticker'].values[0]} ({vol[0].values[0]:.2f})]"
                )

            with col2:
                data_min = (
                    preprocessing.corr_data(data=data).tail(1).min().reset_index()
                )
                min = data_min[data_min[0] == data_min[0].min()]
                st.subheader("Lowest Price : ")
                st.subheader(
                    f":red[{min['ticker'].values[0]} ({min[0].values[0]:.2f})]"
                )

                data_vol = (
                    preprocessing.corr_data(data=data, columns="Volume")
                    .tail(1)
                    .min()
                    .reset_index()
                )
                vol = data_vol[data_vol[0] == data_vol[0].min()]
                st.subheader("Lowest Volume  : ")
                st.subheader(
                    f":red[{vol['ticker'].values[0]} ({vol[0].values[0]:.2f})]"
                )

            with col3:

                mean_vol = (
                    preprocessing.corr_data(data=data, columns="Volume").mean() / 30
                ).reset_index()
                vol_highest = mean_vol[mean_vol[0] == mean_vol[0].min()]
                st.subheader("Lowest Average Volume(30)")
                st.subheader(
                    f":red[{vol_highest['ticker'].values[0]} ({vol_highest[0].values[0]:.2f})]"
                )

                mean_vol = (
                    preprocessing.corr_data(data=data, columns="Volume").mean() / 30
                ).reset_index()
                vol_highest = mean_vol[mean_vol[0] == mean_vol[0].max()]
                st.subheader("Highest Average Volume(30)")
                st.subheader(
                    f":blue[{vol_highest['ticker'].values[0]} ({vol_highest[0].values[0]:.2f})]"
                )

            st.title("Candlestick Chart")
            candle_stock = st.selectbox("select one :", options=stock)
            st.plotly_chart(
                helper.candle_plot(
                    df=data.reset_index(), multi=True, ticker=candle_stock
                )
            )

        with st.expander("Performance Metrics"):

            perfoma_data = preprocessing.calculate_daily_returns_multi(data=data)

            st.title("Daily Returns of Selected Stocks")
            st.plotly_chart(
                helper.plot_daily_returns_dropdown(data=perfoma_data, tickers=stock)
            )

            st.title("Cumulative Returns Chart")
            st.plotly_chart(
                helper.plot_multi_line(
                    data=perfoma_data,
                    hue="ticker",
                    y="Cumulative Return",
                    title="Cumulative Returns Chart",
                )
            )

            st.divider()

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Highest Cumulative Return :")
                max_cum = preprocessing.annot_cum_and_return(
                    data=perfoma_data, operator="max", column="Cumulative Return"
                )
                st.subheader(
                    f":green[{max_cum['ticker']} ({(max_cum['value'] * 100):.2f}]) %"
                )

                st.subheader("Highest Return : ")
                max_return = preprocessing.annot_cum_and_return(
                    data=perfoma_data, operator="max", column="Daily Return"
                )
                st.subheader(
                    f":green[{max_return['ticker']} ({(max_return['value'] * 100):.2f}]) %"
                )

            with col2:
                st.subheader("Lowest Cumulative Return :")
                min_cum = preprocessing.annot_cum_and_return(
                    data=perfoma_data, operator="min", column="Cumulative Return"
                )
                st.subheader(
                    f":red[{min_cum['ticker']} ({(min_cum['value'] * 100):.2f}]) %"
                )

                st.subheader("Lowest Return : ")
                max_return = preprocessing.annot_cum_and_return(
                    data=perfoma_data, operator="min", column="Daily Return"
                )
                st.subheader(
                    f":red[{max_return['ticker']} ({(max_return['value'] * 100):.2f}]) %"
                )

            st.divider()

            st.title("Moving Average")

            col1, col2 = st.columns(2)

            with col1:
                stock_ma = st.selectbox(
                    label="stock : ",
                    options=stock,
                )

            with col2:
                num_ma = st.number_input(
                    "How many moving averages do you want to plot ? ",
                    min_value=1,
                    max_value=5,
                    value=1,
                    step=1,
                )
            ma_values = []
            for i in range(num_ma):
                ma_value = st.slider(
                    f"Moving Average {i+1}",
                    min_value=1,
                    max_value=200,
                    value=20,
                    step=1,
                )
                ma_values.append(ma_value)

            data_moving = preprocessing.Rolling(
                data=data, roll=ma_values, multi=True, stock=stock_ma
            )

            st.plotly_chart(
                helper.Overview_all(
                    data=data_moving, title=f"{stock_ma} Moving Avarage"
                )
            )

            st.title(" Average True Range (ATR)")

            stock_atr = st.selectbox(label="selcet stock : ", options=stock)
            ATR = preprocessing.calculate_atr(data=data, ticker=stock_atr)

            st.info(f"{ATR.rolling_14.iloc[-1]}")
            st.plotly_chart(
                helper.Overview_all(data=ATR, title=(f"Rolling ATR {stock_atr}"))
            )

        with st.expander("Statistical Analysis"):

            st.title("Descriptive Statistics")

            stock_stats = st.selectbox("Select one stock :", options=stock)
            data_stats = data[data.ticker == stock_stats]

            col1, col2, col3 = st.columns(3)

            with col1:
                st.subheader("Mean Return : ")
                st.subheader(
                    f":blue[{( data_stats.Close.pct_change().mean() * 100 ):.3f}] %"
                )
                st.subheader("Skewness Return : ")
                st.subheader(
                    f":blue[{( skew(data_stats.Close.pct_change().dropna()) ):.3f}]"
                )
            with col2:
                st.subheader("Median Return : ")
                st.subheader(
                    f":green[{( data_stats.Close.pct_change().median() * 100):.3f}] %"
                )
                st.subheader("Kurtosis Return : ")
                st.subheader(
                    f":blue[{( kurtosis(data_stats.Close.pct_change().dropna()) ):.3f}]"
                )
            with col3:
                st.subheader("Standar Deviasi Return : ")
                st.subheader(f":green[{( data_stats.Close.pct_change().std()):.3f}]")
                st.subheader("Kurtosis Return : ")
                st.subheader(
                    f":blue[{( kurtosis(data_stats.Close.pct_change().dropna()) ):.3f}]"
                )

            st.title("Correlation Matrix ")

            corr_data = preprocessing.corr_data(data=data)
            st.plotly_chart(helper.heatmap(corr=corr_data.pct_change().corr()))

            col1, col2 = st.columns(2)

            with col1:

                x = st.selectbox("Select X-Axis :", options=stock)
            with col2:

                y = st.selectbox("Select Y-Axis :", options=stock)

            st.title("Scattter Plot")

            st.plotly_chart(helper.scatter_plot(x=x, y=y, data=corr_data))

            col1, col2 = st.columns(2)

            with col1:
                cov = corr_data[x].pct_change().cov(corr_data[y].pct_change())
                st.subheader("Covariance : ")

                if cov >= 0.5:
                    st.success(cov)
                elif cov == 0.5:
                    st.warning(cov)
                else:
                    st.error(cov)

            with col2:

                corr = corr_data[x].pct_change().corr(corr_data[y].pct_change())
                st.subheader("Correlation : ")

                if corr >= 0.5:
                    st.success(corr)
                elif corr == 0.5:
                    st.warning(corr)
                else:
                    st.error(corr)

        with st.expander("Risk and Return Ratios"):

            st.title("Return Ratio")

            ratio_stock = st.selectbox("select one stock : ", options=stock)
            st.divider()

            col1, col2 = st.columns(2)

            data_ratio = data[data.ticker == ratio_stock].drop("ticker", axis=1)

            with col1:
                st.subheader("Sharpe Ratio : ")
                sharpe_ratio = preprocessing.sharpe_ratio(data=data_ratio)
                if sharpe_ratio < 1:
                    st.error(f"{sharpe_ratio:.3f}")
                elif 1 <= sharpe_ratio < 2:
                    st.warning(f"{sharpe_ratio:.3f}")
                else:
                    st.success(f"{sharpe_ratio:.3f}")

                st.subheader("Sortino Ratio : ")
                sortino_ratio = preprocessing.sortino_ratio(data=data_ratio)

                if sortino_ratio < 1:
                    st.error(f"{sortino_ratio:.3f}")
                elif sortino_ratio > 1:
                    st.success(f"{sortino_ratio:.3f}")
                else:
                    None

            with col2:

                st.subheader("Calmar Ratio :")
                Calmar_ratio = preprocessing.calculate_calmar_ratio(data=data_ratio)

                if Calmar_ratio < 1:
                    st.error(f"{Calmar_ratio:.3f}")
                elif Calmar_ratio > 1:
                    st.success(f"{Calmar_ratio:.3f}")
                else:
                    None

                st.subheader("Omega Ratio :")
                Omega_ratio = preprocessing.omega_ratio(data=data_ratio)

                if Omega_ratio > 1:
                    st.success(f"{Omega_ratio:.3f}")
                elif Omega_ratio < 1:
                    st.error(f"{Omega_ratio:.3f}")
                else:
                    None

            st.divider()

            st.title("Expected Return vs Risk ")
            st.plotly_chart(
                helper.risk_plot(
                    rets=preprocessing.corr_data(data=data).pct_change().dropna()
                )
            )
