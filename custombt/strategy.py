from abc import abstractmethod, ABCMeta
# import pandas as pd
from decimal import Decimal as d


class Strategy(metaclass=ABCMeta):
    def __init__(self,
                 cash: float = 10000,
                 coins: float = 0.0,
                 commission: float = .0,
                 tick_size: float = 0.01000000,
                 lot_size: float = 0.00000100,
                 ):
        self._cash = cash
        self._coins = coins
        self._commission = commission
        self.data = None
        self._trade_log = 'HOLD'
        self._tick_size = tick_size
        self._lot_size = lot_size
    
    @abstractmethod
    def next(self):
        '''
        define this method
        '''

    @abstractmethod
    def init(self):
        '''
        define this method
        '''

    def buy(self, size: float = 1.0):
        quantity, price, fee = self._calc_buy(size)
        if quantity:
            self._cash -= price
            self._cash -= fee
            self._coins += quantity
            self._trade_log = 'BUY'
            return True
        return False
    
    def sell(self, size: float = 1.0):
        quantity, price, fee = self._calc_sell(size)
        if quantity:
            self._cash += price
            self._cash -= fee
            self._coins -= quantity
            self._trade_log = 'SELL'
            return True
        return False
    
    def get_trade_log(self):
        last_trade = self._trade_log
        self._trade_log = 'HOLD'
        return last_trade
    
    def set_data(self, data):
        self.data = data

    def get_cash(self):
        return self._cash

    def get_coins(self):
        return self._coins

    def _calc_buy(self, size: float = 1.0):
        current_price = d(str(self.data.Close))
        cash = d(str(self._cash))
        commission = d(str(self._commission))
        size = d(str(size))
        lot_size = d(self._lot_size)

        quantity = cash / (current_price*(size+commission))
        quantity -= quantity%lot_size
        price = quantity*current_price
        fee = price*commission

        return float(quantity), float(price), float(fee)

    def _calc_sell(self, size: float = 1.0):
        current_price = d(str(self.data.Close))
        coins = d(str(self._coins))
        commission = d(str(self._commission))
        size = d(str(size))
        lot_size = d(str(self._lot_size))

        quantity = coins - (coins%lot_size)
        price = quantity*current_price
        fee = price*commission

        return float(quantity), float(price), float(fee)
