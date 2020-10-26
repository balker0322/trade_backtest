import pandas as pd
from custombt.backtest import Backtest
from custombt.strategy import Strategy
from matplotlib import pyplot as plt
import pickle
from random import random

class SmaCross(Strategy):
    
    last_action = 'SELL'

    def init(self):
        pass

    def next(self):
        lo = self.data.sma200
        mid = self.data.sma500
        hi = self.data.sma1000

        if lo > mid and mid > hi and self.last_action == 'SELL':
            self.buy()
            self.last_action = 'BUY'

        elif lo < mid and mid < hi and self.last_action == 'BUY':
            self.sell()
            self.last_action = 'SELL'

# load dataset
btcusdt = pd.read_csv("btcusdt24mo.csv")
# set timestamp as index
btcusdt = btcusdt.rename(columns={'E':'timestamp'})
btcusdt['timestamp'] = pd.to_datetime(btcusdt['timestamp'], unit='ms')
btcusdt = btcusdt.set_index(['timestamp'])
# rename columns
btcusdt = btcusdt.rename( columns={'o':'Open',
                         'h':'High',
                         'l':'Low',
                         'c':'Close',
                         'v':'Volume'},)
# retain open, high, low, close and volume
btcusdt = btcusdt[['Open','High','Low','Close','Volume']]

def add_sma(df, ref, n):
    label = 'sma'+str(n)
    if not label in df.columns:
        df[label] = pd.Series(ref).rolling(n).mean()

# adding sma indicators
add_sma(btcusdt, btcusdt.Close, 200)
add_sma(btcusdt, btcusdt.Close, 500)
add_sma(btcusdt, btcusdt.Close, 1000)
btcusdt = btcusdt.dropna().astype(float)
# btcusdt

bt = Backtest(  data = btcusdt.iloc[0:2000],
                strategy = SmaCross,
                cash = 2000.0,
                coins = 0.0,
                commission = 0.001,
                tick_size = 0.01000000,
                lot_size = 0.00000100,)
bt.run()

with open('btresult', 'wb') as file:
    pickle.dump(bt.activity_log, file)