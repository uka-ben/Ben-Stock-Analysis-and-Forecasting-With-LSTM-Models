import streamlit as st
import pandas as pd
import datetime
import preprocessing
import helper
import time


def Analysis_stock_data(stock_symbol):

    st.title(f":green[{stock_symbol.replace('.JK','')} Stock Data Analysis]")
    st.markdown(
        """
                  **Welcome to the Stock Analysis Dashboard!**

                  Explore various tools and features designed to help you analyze stock performance with ease. Select the stock you wish to analyze and dive deeper into the data through interactive visualizations.
                  Leverage key metrics such as daily returns, cumulative returns, moving averages, and other essential ratios to support your investment decisions.

                  **Start analyzing your stocks now!**
                  """
    )
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        start = st.date_input("Start-Date : ", value=pd.to_datetime("2023-01-01"))
    with col2:
        end = st.date_input(
            "Start-Date : ", value=pd.to_datetime(datetime.date.today())
        )

    if st.button("Retrieve Data and Perform Analysis"):

        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.020)
            progress_bar.progress(i + 1)

        data = preprocessing.Get_Analysis_Data(
            start=start, end=end, ticker=stock_symbol
        )
        data_compare = preprocessing.Get_compare_data(start=start, end=end)

        with st.expander("Display Stock Data"):

            with st.container(height=400):
                st.table(data)
            col1, col2 = st.columns([2, 1])
            with col1:
                st.subheader(f"Total Rows : {data.shape[0]}")
            with col2:
                st.subheader(f"Total Columns : {data.shape[1]}")

        with st.expander("Comprehensive Data Overview"):

            st.title("Graphical Data Representation : ")
            st.plotly_chart(
                helper.Overview_all(data=data, drop=True, title="Volume"),
                use_container_width=True,
            )

            st.divider()
            col1, col2, col3 = st.columns(3)

            with col1:
                st.subheader("Highest Price : ")
                st.subheader(f":green[{data.High.max():.2f}]")
                st.subheader("Most Recent Closing Price")
                st.subheader(f":green[{data.Close.iloc[-1]:.2f}]")

            with col2:
                st.subheader("Lowest Price : ")
                st.subheader(f":red[{data.Low.min():.2f}]")
                st.subheader("Most Recent Opening Price")
                st.subheader(f":red[{data.Open.iloc[-1]:.2f}]")
            with col3:
                st.subheader("Average Price : ")
                st.subheader(f":blue[{data.Close.mean():.2f}]")
                st.subheader("Average Daily Volume")
                st.subheader(f":blue[{(data.Volume.sum()/30):.2f}]")

            st.divider()

            st.title("Volume Data Visualization: ")
            st.plotly_chart(
                helper.line_plot(data=data, column="Volume", color="blue"),
                use_container_width=True,
            )

            st.title("Candlestick Chart")
            st.plotly_chart(helper.candle_plot(df=data.reset_index(), multi=False))

        with st.expander("Return"):

            st.title("Daily Percentage Return :")
            data_return = preprocessing.Get_Return(data=data)
            st.plotly_chart(
                helper.line_plot(data=data_return, column="return", color="blue"),
                use_container_width=True,
            )

            st.title("Cumulative Percentage Return :")
            st.plotly_chart(
                helper.line_plot(
                    data=data_return, column="cumulative return", color="green"
                ),
                use_container_width=True,
            )

            st.divider()

            col1, col2, col3 = st.columns(3)

            with col1:
                st.subheader("Highest Daily Return :")
                st.subheader(f':green[{data_return["return"].max() *100:.2f}] %')
            with col2:
                st.subheader("Lowest Daily Return :")
                st.subheader(f':red[{data_return["return"].min()*100:.2f}] %')
            with col3:
                st.subheader("Average Daily Return :")
                st.subheader(f':green[{data_return["return"].mean()*100:.2f}] %')

            st.subheader("The cumulative return has increased by:")
            st.success(f'{data_return["cumulative return"].iloc[-1]:.2f} %')
            st.divider()

            st.title("Histogram of Daily Returns")
            st.plotly_chart(
                helper.Histplot(
                    data=preprocessing.hist_return_data(data=data),
                    columns="return",
                    title="Histogram Returns",
                )
            )

            st.title("Daily Return Comparison: Stock vs. Benchmark")
            st.plotly_chart(
                helper.Overview_all(
                    data=preprocessing.compare_data_merge(
                        data=data, compare=data_compare
                    ),
                    drop=False,
                    title="Comparison: Stock vs. Benchmark",
                )
            )

            st.divider()

            col1, col2, col3 = st.columns(3)

            data_hist = preprocessing.treshold_return(data=data)

            with col1:
                st.subheader("Total Positive Return :")
                st.subheader(f":green[{data_hist[True]}]")
            with col2:
                st.subheader("Total Negative Return :")
                st.subheader(f":red[{data_hist[False]}]")
            with col3:
                st.subheader("Probability of Positive Return")
                st.subheader(
                    f":green[{(data_hist[True] / (data_hist[True] + data_hist[False])) * 100 :.2f}] %"
                )

            st.divider()
            st.title("Drawdown : ")
            st.plotly_chart(
                helper.drawdown_plot(data=preprocessing.data_drawdown(data=data))
            )

            st.subheader(f"Maximum Drawdown (MDD): ")
            st.error(f"{preprocessing.data_drawdown(data=data).Drawdown.min():.2%}")
            st.subheader(f"Maximum Drawdown Duration :")
            st.error(
                f"{preprocessing.calculate_drawdown_duration(data=preprocessing.data_drawdown(data))} Days"
            )

        with st.expander("Moving Average"):

            st.title("Rolling Moving Average : ")
            st.plotly_chart(
                helper.Overview_all(
                    data=preprocessing.Rolling(data=data),
                    title="Rolling Moving Average",
                )
            )

            st.title("Rolling Volatility : ")
            st.plotly_chart(
                helper.Overview_all(
                    data=preprocessing.Rolling_volatility(data=data),
                    title="Rolling Volatility ",
                )
            )

        with st.expander("Ratio"):

            st.title("Sharpe Ratio :")
            sharpe_ratio = preprocessing.sharpe_ratio(data=data)

            if sharpe_ratio < 1:
                st.error(f"{sharpe_ratio:.3f}")
            elif 1 <= sharpe_ratio < 2:
                st.warning(f"{sharpe_ratio:.3f}")
            else:
                st.success(f"{sharpe_ratio:.3f}")
            st.plotly_chart(
                helper.line_plot(
                    data=preprocessing.sharpe_ratio_rol(data=data),
                    column="rolling sharpe ratio",
                    color="red",
                )
            )

            st.title("Other Ratio :")

            st.divider()

            col1, col2, col3 = st.columns(3)

            with col1:
                st.subheader("Sortino Ratio :")
                sortino_ratio = preprocessing.sortino_ratio(data=data)

                if sortino_ratio < 1:
                    st.error(f"{sortino_ratio:.3f}")
                elif sortino_ratio > 1:
                    st.success(f"{sortino_ratio:.3f}")
                else:
                    None

                st.subheader("Calmar Ratio :")
                Calmar_ratio = preprocessing.calculate_calmar_ratio(data=data)

                if Calmar_ratio < 1:
                    st.error(f"{Calmar_ratio:.3f}")
                elif Calmar_ratio > 1:
                    st.success(f"{Calmar_ratio:.3f}")
                else:
                    None

            with col2:

                st.subheader("Information Ratio :")
                information_ratio = preprocessing.calculate_information_ratio(
                    portfolio_data=data, benchmark_data=data_compare
                )

                if information_ratio > 1:
                    st.success(f"{information_ratio:.3f}")
                elif information_ratio < 1:
                    st.error(f"{information_ratio:.3f}")
                else:
                    None

                st.subheader("Omega Ratio :")
                Omega_ratio = preprocessing.omega_ratio(data=data)

                if Omega_ratio > 1:
                    st.success(f"{Omega_ratio:.3f}")
                elif Omega_ratio < 1:
                    st.error(f"{Omega_ratio:.3f}")
                else:
                    None

            with col3:

                capture_ratio = preprocessing.calculate_capture_ratios(
                    data, benchmark_data=data_compare
                )

                st.subheader("Upside Capture Ratio :")
                st.success(capture_ratio["Upside Capture Ratio"])

                st.subheader("Downside Capture Ratio :")
                st.error(capture_ratio["Downside Capture Ratio"])

            st.divider()
