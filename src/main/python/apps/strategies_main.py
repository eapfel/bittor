import logging

from src.main.python.api.exmo_api import ExmoApi
from src.main.python.strategies.ha_strategy import HaStrategy

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

has = HaStrategy(ExmoApi())
df = has.get_df()
df_ha = has.heikin_ashi(df)
df_trades = has.back_test(df_ha)
# print(df_trades.head(100))
# df_positions = has.execute(df_trades, df_ha.index, 10)
# print(df_positions.head(100))
has.plot_ha_candlestick(df_ha, df_trades)
#wins = - df[1:]['Open'] * df_positions.shift(1)[1:]
#print(f'Wins percentage: {(wins.sum() / df[1:]["Open"].sum() * 100).round(1)}%')

#print(wins.describe())
