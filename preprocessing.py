import yfinance as yf
import plotly.express as px
import plotly.graph_objs as go
import numpy as np
import pandas as pd



def Get_Analysis_Data(start , end , ticker ) : 
    data = yf.download(ticker , start=start , end=end)
    return data

def Get_compare_data(start , end, ticker = '^GSPC'):
    data = yf.download(ticker , start=start , end=end)
    return data

def Get_Return(data , num=100) : 
    data["return"] = data["Close"].pct_change()

    pct = data["Close"].pct_change().add(1)
    cumulative_return = pct.cumprod().sub(1)
    data["cumulative return"] = cumulative_return.mul(num)

    return data

def Rolling(data ,stock=None, roll = [7,30,90,200] , multi=False ) : 

    if multi == True :
        data = data[data.ticker == stock]
    data = data.filter(['Close'])

    for w in roll : 
       data[w] = data.Close.rolling(window=w).mean()
    
    return data

def Rolling_volatility(data) : 
    data = data.filter(['Close'])
    data["return"] = data.pct_change()
    data['rolling_7'] = data["return"].rolling(window=7).std()
    data['rolling_30'] = data["return"].rolling(window=30).std()
    data['rolling_90'] = data["return"].rolling(window=90).std()


    return data[['rolling_7','rolling_30','rolling_90']]

def sharpe_ratio(data) : 
    risk = 0.02/225

    data['returns'] = data['Close'].pct_change(1)
    data['excess_returns'] = data['returns'] - risk

    sharpe_ratio = np.sqrt(252) * data['excess_returns'].mean() / data["excess_returns"].std()
    return sharpe_ratio

def sharpe_ratio_rol(data) : 
    rolling_window = 30 

    rolling_mean = data['excess_returns'].rolling(window=rolling_window).mean()
    rolling_std = data['excess_returns'].rolling(window=rolling_window).std()

    rolling_sharpe = np.sqrt(252) * rolling_mean / rolling_std

    data['rolling sharpe ratio'] = rolling_sharpe

    return data

def hist_return_data(data):
    data["return"] = data['Close'].pct_change()

    return data.filter(['return'])

def compare_data_merge (data , compare) :

    data = data.filter(['Close']).pct_change()
    data.columns = ['Close']
    compare = compare.filter(['Close']).pct_change()
    compare.columns = [f'comparations']

    final_data = pd.concat([data , compare] , axis=1)
    return final_data


def data_drawdown(data) : 
    
    data['Peak'] = data['Close'].cummax()  
    data['Drawdown'] = (data['Close'] - data['Peak']) / data['Peak']

    return data

def treshold_return(data) : 
    data['return'] = data.filter(['Close']).pct_change()

    data['is_true'] = np.where(data['return'] >= 0 , True , False)

    data = data.value_counts('is_true')

    return data


def calculate_drawdown_duration(data):
    
    drawdown_starts = data[data['Drawdown'] < 0].index
    drawdown_ends = data[data['Close'] >= data['Peak']].index
    
    durations = []
    for start in drawdown_starts:
        end = drawdown_ends[drawdown_ends >= start]
        if not end.empty:
            duration = (end[0] - start).days
            durations.append(duration)
    
    if not durations:
        return None
    
    max_duration = max(durations)
    
    return max_duration

def sortino_ratio(data, target_return=0.02):
    data['returns'] = data['Close'].pct_change()
    
    mean_return = data['returns'].mean()
    
    downside_returns = data['returns'][data['returns'] < target_return]
    downside_deviation = np.sqrt((downside_returns - target_return).pow(2).mean())
    
    sortino_ratio = (mean_return - target_return) / downside_deviation
    
    return sortino_ratio

def calculate_calmar_ratio(data):

    initial_value = data['Close'].iloc[0]
    final_value = data['Close'].iloc[-1]
    periods = len(data) / 252  
    cagr = (final_value / initial_value) ** (1 / periods) - 1

    max_drawdown = data_drawdown(data).Drawdown.min()    

    calmar_ratio = cagr / max_drawdown if max_drawdown != 0 else np.nan
    
    return calmar_ratio



def calculate_information_ratio(portfolio_data, benchmark_data):

    portfolio_data['returns'] = portfolio_data['Close'].pct_change()
    benchmark_data['returns'] = benchmark_data['Close'].pct_change()
    
    common_index = portfolio_data.index.intersection(benchmark_data.index)

    portfolio_returns = portfolio_data.loc[common_index, 'returns']
    benchmark_returns = benchmark_data.loc[common_index, 'returns']
    
    active_return = portfolio_returns - benchmark_returns
    tracking_error = active_return.std()
    information_ratio = active_return.mean() / tracking_error if tracking_error != 0 else np.nan
    
    return information_ratio

def omega_ratio(data, threshold=0.02):
 
    data['returns'] = data['Close'].pct_change().dropna()
    
    above_threshold = data['returns'][data['returns'] > threshold].sum()
    below_threshold = -data['returns'][data['returns'] < threshold].sum()  
    
    omega_ratio_value = above_threshold / below_threshold if below_threshold != 0 else np.nan
    
    return omega_ratio_value

def calculate_capture_ratios(investment_data, benchmark_data):

    investment_data['returns'] = investment_data['Close'].pct_change().dropna()
    benchmark_data['returns'] = benchmark_data['Close'].pct_change().dropna()
    
    common_index = investment_data.index.intersection(benchmark_data.index)
    investment_returns = investment_data.loc[common_index, 'returns']
    benchmark_returns = benchmark_data.loc[common_index, 'returns']
    
    up_market = benchmark_returns > 0
    down_market = benchmark_returns < 0
    
    upside_capture = investment_returns[up_market].mean() / benchmark_returns[up_market].mean() * 100 if benchmark_returns[up_market].mean() != 0 else np.nan
    downside_capture = investment_returns[down_market].mean() / benchmark_returns[down_market].mean() * 100 if benchmark_returns[down_market].mean() != 0 else np.nan
    
    return {
        'Upside Capture Ratio': upside_capture,
        'Downside Capture Ratio': downside_capture
    }

def calculate_beta(stock_returns, market_returns):
    covariance = np.cov(stock_returns, market_returns)[0, 1]
    
    variance_market = np.var(market_returns)
    
    # Menghitung Beta
    beta = covariance / variance_market
    
    return beta

def download_multistock_data(tickers, start_date, end_date):
    data = yf.download(tickers, start=start_date, end=end_date, group_by='ticker')

    df_list = []
    for ticker in tickers:
        df = data[ticker].copy() 
        df['ticker'] = ticker 
        df_list.append(df)   

    final_data = pd.concat(df_list)

    return final_data

def calculate_daily_returns_multi(data):
   
    data = data.copy()
    data['Daily Return'] = data.groupby('ticker')['Close'].pct_change()
    data['Cumulative Return'] = (1 + data['Daily Return']).groupby(data['ticker']).cumprod() - 1
    return data

def calculate_atr(data , ticker) : 

    stock_data = data[data.ticker == ticker]

    stock_data['high-low'] = stock_data['High'] - stock_data['Low']
    stock_data['high-close'] = (stock_data['High'] - stock_data['Close'].shift()).abs()
    stock_data['low-close'] = (stock_data['Low'] - stock_data['Close'].shift()).abs()
    stock_data['true_range'] = stock_data[['high-low', 'high-close', 'low-close']].max(axis=1)
    stock_data["rolling_14"] = stock_data['true_range'].rolling(window=14).mean()
    stock_data["rolling_30"] = stock_data['true_range'].rolling(window=30).mean()

    return stock_data[['rolling_14' , 'rolling_30']]

def corr_data(data, columns='Close') : 
    return data.pivot_table(index='Date' , columns='ticker' , values=columns)


def annot_cum_and_return(data , operator , column):

    subset = data.groupby(['ticker'])[column].last().reset_index()
    if operator == "max":
        result = subset[subset[column] == subset[column].max()]
    elif operator == "min" : 
        result = subset[subset[column] == subset[column].min()]
    
    return {"ticker" : result['ticker'].values[0],
             "value" : result[column].values[0]}




