import pandas as pd
import numpy as np
import pickle
from tqdm import tqdm

filename = 'btcusdt24mo'

# ============================================== #
#                  process data                  #
# ============================================== #

# load dataset
data = pd.read_csv("data/" + filename + ".csv")

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
ema_size = 100
price = data.Close
ema_table = np.empty((len(price),ema_size), float)
ema_factor = np.linspace(.0001, 1.0, ema_size)
price_old = price[0]
for i in tqdm(range(len(price))):
    current_price = price[i]
    ema_table[i] = (1.0 - ema_factor)*price_old + ema_factor*current_price
    price_old = current_price

# to file
with open('data/' + filename + '_ema_table', 'wb') as file:
    pickle.dump(ema_table, file)