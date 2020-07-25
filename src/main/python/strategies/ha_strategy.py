import numpy as np
import pandas as pd
import plotly.graph_objects as go
from pandas import DataFrame

from src.main.python.api.bitcoin_api import BitcoinApi


class HaStrategy:
    def __init__(self, api: BitcoinApi):
        self.api = api

    def get_df(self):
        df = self.api.get_data_frame_history()
        return df

    def heikin_ashi(self, df):
        ha_close = (df['Open'] + df['Close'] + df['High'] + df['Low']) / 4

        ha_open = [(df['Open'].iloc[0] + df['Close'].iloc[0]) / 2]
        for close in ha_close[:-1]:
            ha_open.append((ha_open[-1] + close) / 2)

        ha_open = np.array(ha_open)

        elements = df['High'], df['Low'], ha_open, ha_close
        ha_high, ha_low = np.vstack(elements).max(axis=0), np.vstack(elements).min(axis=0)

        return pd.DataFrame({
            'ha_open': ha_open,
            'ha_high': ha_high,
            'ha_low': ha_low,
            'ha_close': ha_close
        })

    def trades(self, df):
        current = df[1:]
        previous = df.shift(1)[1:]

        latest_bearish = current['ha_close'] < current['ha_open']
        previous_bearish = previous['ha_close'] < previous['ha_open']

        current_candle_longer = (
                np.abs(current['ha_close'] - current['ha_open'])
                > np.abs(previous['ha_close'] - previous['ha_open']))

        current_open_eq_high = current['ha_open'] == current['ha_high']
        current_open_eq_low = current['ha_open'] == current['ha_low']

        long = (
                latest_bearish
                & current_candle_longer
                & previous_bearish
                & current_open_eq_high)
        short = (
                ~latest_bearish
                & current_candle_longer
                & ~previous_bearish
                & current_open_eq_low)

        long_exit = (
                ~latest_bearish
                & ~previous_bearish
                & current_open_eq_low)
        short_exit = (
                latest_bearish
                & previous_bearish
                & current_open_eq_high)

        return pd.DataFrame(
            {'long': long,
             'short': short,
             'long_exit': long_exit,
             'short_exit': short_exit},
            index=current.index)

    def back_test(self, df: DataFrame, position=5000):

        runs = 0
        red = 0
        green = 0
        buy = True
        btc = 0
        buy_dic = []
        sell_dic = []
        fee = 0.2 / 100
        stop_loss = 0
        for i in range(0, df.shape[0]):

            ha = df.iloc[i]

            ha['ha_bullish'] = 0

            if ha['ha_open'] > ha['ha_close']:
                ha['ha_bullish'] = -1

            if (ha['ha_low'] == ha['ha_open']) & (ha['ha_open'] < ha['ha_close']):
                ha['ha_bullish'] = 1

            if ha['ha_bullish'] == 1:
                green += 1
                red -= 1
            elif ha['ha_bullish'] == -1:
                red = 1 + red if buy else 1
                green = 0
            else:
                green = 0

            if (green == 4) & (runs >= 5) & (red != 5) & buy:
                red = 0
                buy = False
                btc = (position * (1 - fee)) / ha['ha_open']
                position = 0
                stop_loss = ha['ha_open']
                print(f'buy {runs} -> btc:{btc}, position:{position}')
                ha['buy'] = True
                ha['sell'] = False
                buy_dic.append(ha['ha_open'])
                sell_dic.append(0)
            elif (red == 1) & (not buy):
                buy = True
                green = 0
                red = 0
                position = (btc * ha['ha_close']) * (1 - fee)
                btc = 0
                print(f'sell {runs} -> btc:{btc}, position:{position}')
                ha['sell'] = True
                ha['buy'] = False
                buy_dic.append(0)
                sell_dic.append(ha['ha_close'])
            elif (not buy) & (((stop_loss / ha['ha_close'] - 1) * 100) >= 1):
                buy = True
                green = 0
                red = 0
                position = (btc * ha['ha_close']) * (1 - fee)
                btc = 0
                print(f'sell {runs} -> btc:{btc}, position:{position}')
                ha['sell'] = True
                ha['buy'] = False
                buy_dic.append(0)
                sell_dic.append(ha['ha_close'])
            else:
                buy_dic.append(0)
                sell_dic.append(0)

            # print('-------')
            # print(res)
            runs += 1

        last_ha = df.iloc[-1]
        if position == 0:
            print(f'position: {btc * last_ha["ha_close"]}, btc: {0}')
        else:
            print(f'position: {position}, btc: {btc}')

        return pd.DataFrame(
            {'buy': buy_dic,
             'sell': sell_dic
             },
            index=df.index
        )

    def execute(self, trades, original_index, initial_position=0):
        positions = [initial_position]

        for _, trade in trades.iterrows():
            position = positions[-1]
            bought, sold = position > 0, position < 0

            close_buy = bought and trade['long_exit']
            close_sell = sold and trade['short_exit']

            positions.append(
                1 if trade['long'] else (
                    -1 if trade['short'] else (
                        0 if (close_buy or close_sell) else (
                            position))))

        return pd.Series(
            positions,
            index=original_index,
            name='positions')

    def plot_ha_candlestick(self, df, df_trades: DataFrame):

        annotations = []

        for index, item in df_trades.iterrows():
            if item['buy'] > 0:
                annotations.append(go.layout.Annotation(x=index,
                                                        y=item['buy'],
                                                        showarrow=True,
                                                        arrowhead=2,
                                                        ax=0,
                                                        ay=30,
                                                        arrowcolor="green",
                                                        arrowsize=2,
                                                        arrowwidth=2,
                                                        text="buy"))
            elif item['sell'] > 0:
                annotations.append(go.layout.Annotation(x=index,
                                                        y=item['sell'],
                                                        showarrow=True,
                                                        ax=0,
                                                        ay=-30,
                                                        arrowhead=2,
                                                        arrowcolor="red",
                                                        arrowsize=2,
                                                        arrowwidth=2,
                                                        text="sell"))

        candlestick = go.Candlestick(
            x=df.index,
            open=df['ha_open'],
            high=df['ha_high'],
            low=df['ha_low'],
            close=df['ha_close']
        )

        fig = go.Figure(data=[candlestick])

        fig.update_layout(
            width=1024, height=764,
            title="BTC/USD",
            yaxis_title='USD',
            annotations=annotations
        )

        fig.show()
