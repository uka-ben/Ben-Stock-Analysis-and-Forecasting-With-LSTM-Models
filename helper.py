import plotly.express as px
import plotly.graph_objs as go
import plotly.io as pio
import numpy as np

pio.templates.default = "plotly"

def line_plot(data , column , color):
    fig = px.line(data, x=data.index, y=column, title=f'Stock {column} Price')
    fig.update_traces(line_color=color)
    return fig


def Overview_all(data , title , drop=False) : 
    if drop == True:
      data = data.drop("Volume" , axis=1)
    
    fig = go.Figure()

    for column in data.columns:
        fig.add_trace(go.Scatter(x=data.index, y=data[column], mode='lines', name=column))

    fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title='Value',
        legend_title='Columns'
    )

    return fig

def Histplot(data , columns , title) : 

    fig = px.histogram(data, x=columns, nbins=50, title=title , marginal="violin")
    fig.update_layout(xaxis_title=columns, yaxis_title="Frequency")

    return fig

def drawdown_plot(data) : 
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=data.index, y=data['Drawdown'], mode='lines', name='Drawdown',
                            line=dict(color='red'), fill='tozeroy'))

    fig.update_layout(
        title='Drawdown Analysis',
        xaxis_title='Date',
        yaxis_title='Drawdown',
        yaxis=dict(tickformat='.0%')
    )

    return fig



def plot_with_dropdown(data, tickers):

    data = data.reset_index()
    
    columns = ['Open', 'High', 'Low', 'Close', 'Volume']

    fig = go.Figure()

    for col in columns:
        for ticker in tickers:
            ticker_data = data[data['ticker'] == ticker]
            fig.add_trace(go.Scatter(
                x=ticker_data['Date'],
                y=ticker_data[col],
                mode='lines',
                name=f"{ticker} - {col}",
                visible='legendonly' if col != 'Close' else True  
            ))

    dropdown_buttons = [
        dict(
            label=col,
            method="update",
            args=[{"visible": [col in trace.name for trace in fig.data]},
                  {"title": f"Stock Prices ({col})"}]
        ) for col in columns
    ]

    fig.update_layout(
        updatemenus=[dict(
            buttons=dropdown_buttons,
            direction="down",
            showactive=True,
        )],
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        legend_title="Ticker"
    )

    return fig

def plot_daily_returns_dropdown(data, tickers):
 
    fig = go.Figure()

    for ticker in tickers:
        ticker_data = data[data['ticker'] == ticker]
        fig.add_trace(
            go.Scatter(
                x=ticker_data.index,
                y=ticker_data['Daily Return'],
                mode='lines',
                name=ticker,
                visible='legendonly' )
        )

    fig.data[0].visible = True

    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Daily Return',
        updatemenus=[{
            'buttons': [
                {'label': ticker,
                 'method': 'update',
                 'args': [{'visible': [ticker == t for t in tickers]}]}
                for ticker in tickers
            ],
            'direction': 'down',
            'showactive': True
        }],
        height=600
    )

    return fig

def plot_multi_line(data , hue , y , title='Closing Prices of Selected Stocks'):

    
    fig = px.line(data, x=data.index, y=y,color=hue, title=title)
    
    return fig

def heatmap(corr) : 

    return px.imshow(corr,text_auto=True,  title='Matriks Korelasi Return Saham')

def scatter_plot(x,y,data) : 
    # Membuat scatter plot
    fig = px.scatter(
        data, 
        x=x, 
        y=y, 
        title='Scatter Plot',
        color_discrete_sequence=['blue'],   
        labels={'x': x, 'y': y}
    )

    return fig

def scatter_matrix(data) : 
    col = data.columns
    
    fig = px.scatter_matrix(
    data,
    dimensions=col,  # Daftar kolom yang akan ditampilkan
    title='Pair Plot menggunakan Plotly Express',
    labels={'x1': 'Feature 1', 'x2': 'Feature 2', 'x3': 'Feature 3'})

    return fig


def risk_plot(rets) : 
# Membuat area ukuran lingkaran
    area = np.pi * 20

    # Buat figure
    fig = go.Figure()

    # Tambahkan scatter plot
    fig.add_trace(go.Scatter(
        x=rets.mean(),  # Mean (Expected return)
        y=rets.std(),   # Standard deviation (Risk)
        mode='markers',
        marker=dict(
            size=area,
            color='blue',
            opacity=0.7
        ),
        text=rets.columns  # Label saham
    ))

    # Tambahkan anotasi untuk setiap saham
    for label, x, y in zip(rets.columns, rets.mean(), rets.std()):
        fig.add_annotation(
            x=x, y=y,
            text=label,
            showarrow=True,
            arrowhead=1,
            ax=50, ay=50,
            arrowcolor='blue'
        )

    # Update layout untuk menambah label sumbu
    fig.update_layout(
        title="Expected Return vs Risk",
        xaxis_title="Expected Return",
        yaxis_title="Risk (Standard Deviation)",
        showlegend=False,
        height=600

    )

    return fig


def candle_plot(df,ticker=None, multi=False) :

    if multi == True : 
        df = df[df.ticker == ticker]
    
    
    

    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                    open=df['Open'], high=df['High'],
                    low=df['Low'], close=df['Close'])])

    # Menambahkan judul dan layout
    fig.update_layout(title='Candlestick Chart',
                    xaxis_title='Date',
                    yaxis_title='Price')
    
    return fig
    

def predictions_plot(data_train , val) : 
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=data_train.index, y=data_train['Close'], mode='lines', name='Train',
                            line=dict(color='red')))
    
    fig.add_trace(go.Scatter(x=val.index, y=val['Close'], mode='lines', name='Test',
                            line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=val.index, y=val['prediction'], mode='lines', name='prediction',
                            line=dict(color='green')))
    fig.update_layout(
        title='Prediction Plot',
        xaxis_title='Date',
        yaxis_title='Price',
    )

    return fig


