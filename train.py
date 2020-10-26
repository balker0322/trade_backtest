from agent.agent import Agent
import pandas as pd
import numpy as np
from custombt.backtest import Backtest
from custombt.strategy import Strategy


# ============================================== #
#                  process data                  #
# ============================================== #

# load dataset
data = pd.read_csv("data/btcusdt24mo.csv")

# set first column as index
old_name = [name for name in data]
data = data.rename(columns={old_name[0]:'timestamp'})
data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
data = data.set_index(['timestamp'])

# rename columns
column_names = ['Open', 'High', 'Low', 'Close', 'Volume']
columns = {old_name[i+1]:column_name for i, column_name in enumerate(column_names)}
data = data.rename( columns=columns,)

# retain open, high, low, close and volume
data = data[column_names]

# create EMA table
ema_size = 1000
ema_table = np.empty((0,ema_size), float)
ema_factor = np.linspace(.0001, 1.0, ema_size)
price = data.Close
price_old = price[0]
for current_price in price:
    current_ema = (1.0 - ema_factor)*price_old + ema_factor*current_price
    ema_table = np.append(ema_table, current_ema.reshape(1, ema_size), axis = 0)
    price_old = current_price


# ============================================== #
#               build startegy class             #
# ============================================== #

class train_model(Strategy):

    def init(self):
        pass

    def next(self):
        pass

# run training
bt = Backtest(  data = data,
                strategy = train_model,
                cash = 2000.0,
                coins = 0.0,
                commission = 0.001,
                tick_size = 0.01000000,
                lot_size = 0.00000100,)
bt.run()

# save model