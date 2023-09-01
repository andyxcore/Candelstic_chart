import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.offline import init_notebook_mode, iplot
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.io as pio
import argparse


pio.renderers.default = "browser"


def read_data(filename='data/prices.csv', timestamp_col='TS'):
    try:
        df = pd.read_csv(filename)
    except FileNotFoundError:
        print(f"No filename: {filename}")
        raise
    try:
        df[timestamp_col] = df[timestamp_col].astype("datetime64[ns]")
        df = df.set_index("TS")
    except KeyError:
        print(f"No 'TS' columns in dataframe, attempt to get")
    return df


def resampled_low(res):
    return res.min()


def resampled_high(res):
    return res.max()


def resamples_first(res):
    return res.first()


def resampled_last(res):
    return res.last()


def resampled_mean(res):
    # """mean value in window"""
    return res.mean()


def resampled_count(res):
    return res.count()


def dec(df, func):
    return func(df)


def calculate_candles(df: pd.DataFrame, n_sec: int = 30):
    """
    calculate data for given time period in seconds
    """
    delta = pd.Timedelta(seconds=n_sec)
    resampled = df.resample(delta)  # resample data using given time period

    # """Score statistics"""
    low = resampled_low(resampled)
    high = resampled_high(resampled)
    mean = resampled_mean(resampled)  # this is for EMA
    open_pr = resamples_first(resampled)
    close_pr = resampled_last(resampled)
    volume = resampled_count(resampled)
    #     Combine into dataframe
    data = {
        "High": high.values.reshape(-1),
        "Low": low.values.reshape(-1),
        "Open": open_pr.values.reshape(-1),
        "Close": close_pr.values.reshape(-1),
        "Mean": mean.values.reshape(-1),
        "Volume": volume.values.reshape(-1),
    }
    merge = pd.DataFrame(data=data, columns=['High', 'Low', 'Open', 'Close', 'Mean', 'Volume'],
                         index=high.index).dropna()
    return merge


def calculate_EMA(df: pd.DataFrame, n_days: int = 1):
    """Get exponential moving average"""
    return df.ewm(times=df.index, halflife=pd.Timedelta(days=n_days)).mean()


def draw_figures(candles: pd.DataFrame, EMA: pd.DataFrame):
    #     make Candlestick
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Candlestick(
            x=candles.index,
            open=candles['Open'],
            high=candles['High'],
            low=candles['Low'],
            close=candles['Close'], name='Candlestick'),
        secondary_y=True
    )

    # add EMA
    trace = go.Scatter(
        x=EMA.index,
        y=EMA.values,
        name='EMA',
        marker=dict(
            color='rgb(34,163,192)'
        ))

    fig.add_trace(trace, secondary_y=True)

    # todo: add volume
    # fig.add_trace(go.Bar(x=candles.index, y=candles['Volume']), secondary_y=False)

    fig['layout'].update(
        width=800,
        height=600,
        title="Candleplot",
        xaxis_domain=[0.05, 1.0],
        xaxis=dict(tickangle=-90),
        # yaxis2=dict(showgrid=False)
    )
    fig.show()
    # pio.show(fig, renderer='browser')
    return fig


def main(data_path, time_inter, EMA_inter):
    stock_data = read_data(data_path, 'TS')
    candles_df = calculate_candles(stock_data, time_inter)
    EMA = calculate_EMA(candles_df['Close'], EMA_inter)
    fig = draw_figures(candles_df, EMA)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path',
                        required=False,
                        default='./data/prices.csv',
                        type=str)

    parser.add_argument('--time_inter', type=int,
                        default=3600,
                        help='time interval in seconds')

    parser.add_argument('--EMA_inter', type=int,
                        default=1,
                        help='number of days for Exp Moving Average')

    args = parser.parse_args()
    print(args)
    main(**vars(args))
