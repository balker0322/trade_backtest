from agent.agent import Agent
import pandas as pd
import numpy as np
from custombt.backtest import Backtest
from custombt.strategy import Strategy
from random import randint


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

# set parameters for sampling
min_initial_samples = 1000
start_index = randint(min_initial_samples, len(data))
episode_len = len(data) - start_index
eval_data = data.iloc[start_index:]
eval_ema_table = ema_table[start_index:]

class train_model(Strategy):
    agent = Agent(ema_size + 1)

    def init(self):
        self.index = 0
        self.state = self.get_state(eval_ema_table[0])

    def next(self):
        action = self.agent.act(self.state) # planned action

        if action == 0 and self.get_current_position() == 1:
            action = 0 if self.sell() else 1 # get the actual action

        elif action == 1 and self.get_current_position() == 0:
            action = 1 if self.buy() else 0 # get the actual action

        next_state = self.get_state(eval_ema_table[self.index + 1])
        reward = 0 # todo
        done = 0 # todo
        self.agent.memory.append((self.state, action, reward, next_state, done))
        self.index += 1
        self.state = next_state

    def get_state(self, ema):
        ema = ema.copy
        mean = np.mean(ema)
        std = np.std(ema)
        ema = (ema - mean) / std
        ema -= ema[0]
        return np.append(ema, float(self.get_current_position()))
    
    def get_current_position(self):
        current_cash_value = self.get_cash()
        current_coin_value = self.get_coins() * self.data.Close
        if current_cash_value > current_coin_value:
            return 0
        return 1

# run training
bt = Backtest(  data = eval_data,
                strategy = train_model,
                cash = 2000.0,
                coins = 0.0,
                commission = 0.001,
                tick_size = 0.01000000,
                lot_size = 0.00000100,)
bt.run()

# save model