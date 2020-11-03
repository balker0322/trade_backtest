from agent.agent import Agent
import pandas as pd
import numpy as np
from custombt.backtest import Backtest
from custombt.strategy import Strategy
from random import randint, random
from functions import *
import os


data = load_pd(csv_path = data_file)
ema_table = load_ema_table(file_path = ema_table_file)
ema_size = 100
min_initial_samples = 20000
episode_len = int()
start_index = int()
eval_data = None
eval_ema_table = None
batch_size = 10
try:
    e = max([int(entry[len('model_ep'):]) for entry in os.listdir('models/')]) + 1
    agent = Agent(ema_size + 1, is_eval=True, model_name='model_ep'+str(e-1))
    print('loading ' + 'model_ep'+str(e-1))
except:
    e = 1
    agent = Agent(ema_size + 1)

class train_model(Strategy):

    def init(self):
        self.index = 0
        self.set_data(eval_data.iloc[self.index]) # to get initial price for inititial position assesment
        self.state = self.get_state(ema=eval_ema_table[self.index])
        self.equity = self.get_equity(current_price=eval_data.iloc[self.index].Close)
        self.initial_equity = self.equity

    def next(self):
        action = agent.act(self.state) # planned action
        current_position = self.get_current_position()
        action_log = 'HOLD'

        if action == 0 and current_position == 1:
            action = 1
            if self.sell():
                action = 0 # get the actual action
                action_log = 'SELL'
                print('sell...')

        elif action == 1 and current_position == 0:
            action = 0
            if self.buy():
                action = 1 # get the actual action
                action_log = 'BUY'
                print('buy...')

        next_state = self.get_state(ema=eval_ema_table[self.index + 1])
        next_equity = self.get_equity(current_price=eval_data.iloc[self.index + 1].Close)

        '''
        price is in usdt / btc

        if position is in usdt (last action = 0)
          good if price goes down
          bad if price goes up

        if position is in btc (last action = 1)
          good if price goes up
          bad if price goes down
        '''


        reward = (next_equity / self.equity) - 1.0
        agent.memory.append((self.state, action, reward, next_state))
        self.index += 1
        self.state = next_state
        self.equity = next_equity
        
        # if len(agent.memory) > batch_size:
        #     agent.expReplay(batch_size)
        
        profit = self.equity/self.initial_equity - 1.0
        self.status_display['profit'] = ('>' if profit < 0.0 else '> ') + "{0:.4f} % ({1:.2f} USDT)".format(profit*100, self.equity)
        self.status_display['action'] = action_log

    def get_state(self, ema):
        ema = ema.copy()
        mean = np.mean(ema)
        std = np.std(ema)
        ema = (ema - mean) / std
        ema -= ema[0]
        state_array = np.empty((1, agent.state_size), float)
        state_array[0][:-1] = ema
        state_array[0][-1] = float(self.get_current_position())
        return state_array
    
    def get_current_position(self):
        current_cash_value = self.get_cash()
        current_coin_value = self.get_coins() * self.data.Close
        if current_cash_value > current_coin_value:
            return 0
        return 1
    
    def get_equity(self, current_price):
        return self.get_cash() + current_price * self.get_coins()

while True:
    print('Episode {}:'.format(e))
    episode_len = randint(1000, 5000)
    start_index = randint(min_initial_samples, len(data) - episode_len)
    eval_data = data.iloc[start_index:start_index+episode_len]
    eval_ema_table = ema_table[start_index:start_index+episode_len]

    bt = Backtest(  data = eval_data.iloc[:-1],
                strategy = train_model,
                cash = 10000.0*random(),
                coins = 1.0*random(),
                commission = 0.001,
                tick_size = 0.01000000,
                lot_size = 0.00000100,)

    bt.run()

    # agent.model.save("models/model_ep" + str(e))

    e += 1

# print('Episode {}:'.format(e))
# episode_len = randint(50000, 70000)
# start_index = randint(min_initial_samples, len(data) - episode_len)
# eval_data = data.iloc[start_index:start_index+episode_len]
# eval_ema_table = ema_table[start_index:start_index+episode_len]

# bt = Backtest(  data = eval_data.iloc[:-1],
#             strategy = train_model,
#             cash = 0.0,
#             coins = 1.0,
#             commission = 0.001,
#             tick_size = 0.01000000,
#             lot_size = 0.00000100,)

# bt.run()