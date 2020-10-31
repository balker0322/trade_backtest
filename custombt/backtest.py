from .strategy import Strategy
import pandas as pd
from typing import Type
from tqdm import tqdm
from time import time as t


class Backtest():    
    def __init__(self,
                 data: pd.DataFrame,
                 strategy: Type[Strategy],
                 cash: float = 10000,
                 coins: float = 0.0,
                 commission: float = 0.0,
                 tick_size: float = 0.01000000,
                 lot_size: float = 0.00000100,
                 ):
        self._data = data
        self._strategy = strategy
        self._cash = cash
        self._coins = coins
        self._commission = commission
        self.activity_log = pd.DataFrame()
        self._tick_size = tick_size
        self._lot_size = lot_size

    def run(self):
        # initialize strategy
        strategy = self._strategy(  cash=self._cash,
                                    coins=self._coins,
                                    commission=self._commission,
                                    tick_size=self._tick_size,
                                    lot_size=self._lot_size,
                                    )
        strategy.init()

        data_size = len(self._data)
        print('creating empty data frame...')
        start_time = t()
        self.activity_log = pd.DataFrame([pd.Series(
                                                    data = {'Close':None,
                                                            'Equity':None,
                                                            'Buy':None,
                                                            'Sell':None,
                                                            'Trade':None,}
                                                            )]*data_size)
        print('empty data frame created: {0:.2f} ms'.format((t() - start_time)*1000))

        # loop for all data
        bar = tqdm(range(data_size))
        time1 = 0
        current_price = self._data.iloc[0].Close
        initial_equity = self._cash + current_price * self._coins

        for i in bar:

            # upadate cash, coins, and equity for every loop
            data = self._data.iloc[i]
            strategy.set_data(data)
            strategy.next()

            # calculate equity
            current_price = data.Close
            equity = strategy.get_cash() + current_price * strategy.get_coins()
            trade = strategy.get_trade_log()
            buy_price = None
            sell_price = None

            if trade == 'BUY':
                buy_price = current_price
            elif trade == 'SELL':
                sell_price = current_price

            # log activity
            start_time = t()
            self.activity_log.iloc[i] = pd.Series(  name = data.name,
                                                    data = {'Close':current_price,
                                                            'Equity':equity,
                                                            'Buy':buy_price,
                                                            'Sell':sell_price,
                                                            'Trade':trade,})
            activity_log_time = t()

            alpha = 0.1
            time1 = (1.0-alpha)*time1 + alpha*(activity_log_time - start_time)*1000
            bar.set_postfix(ordered_dict={  "activity_log_time":"{0:.2f} ms".format(time1),
                                            "Equity":"{0:.2f}% ({1:.2f} USDT)".format((equity/initial_equity)*100, equity)
                                            })
    
    def plot(self):
        pass
                
    
    # def _get_exchange_info(self):
    #     file_name = self._exchange_file_name
    #     # x = client.get_exchange_info() # file is generated by this command from binance
    #     with open(file_name,'rb') as file:
    #         x =  pickle.load(file)
    #         # get only filter info
    #         info = {q['symbol']:{w['filterType']:w for w in q['filters']} for q in x['symbols']}
    #         self._exchange_info = info[self._pairs]