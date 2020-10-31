import pickle
import pandas as pd

data_folder = 'data/'
data_file = data_folder + 'btcusdt24mo.csv'
ema_table_file = data_folder + 'btcusdt24mo_ema_table'

# ============================================== #
#                  process data                  #
# ============================================== #

def load_pd(csv_path:str):
    # load dataset
    data = pd.read_csv(csv_path)

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
    return data[column_names]

def load_ema_table(file_path:str):
    # create EMA table
    ema_table = None
    with open('data/btcusdt24mo_ema_table', 'rb') as file:
        ema_table = pickle.load(file)
    return ema_table