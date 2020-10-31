import os
from dotenv import load_dotenv
from binance.client import Client
import pickle
import pandas as pd

load_dotenv()

BINANCE_CREDENTIALS = {
    'KEY': os.environ.get('BINANCE_KEY'),
    'SECRET': os.environ.get('BINANCE_SECRET'),
}

data_folder = 'data/'
pickle_file_name = data_folder+'kline'
number_of_months = '24'


def download_historical():
    client = Client(BINANCE_CREDENTIALS['KEY'], BINANCE_CREDENTIALS['SECRET'])

    klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, number_of_months+" month ago UTC")

    with open(pickle_file_name, 'wb') as file:
        pickle.dump(klines, file)

def convert_to_csv():
    with open(pickle_file_name, 'rb') as file:
        klines = pickle.load(file) 
        # for line in klines:
        #     del line[6:]
        df = pd.DataFrame(klines, columns=['E', 'o', 'h', 'l', 'c', 'v', 
                                            'close time',
                                            'quote asset volume',
                                            'number of trades',
                                            'taker buy base asset volume',
                                            'taker buy quote asset volume',
                                            'ignore'])
        df.set_index('E', inplace=True)
        df.to_csv(data_folder+'btcusdt'+number_of_months+'mo.csv')



def main():
    download_historical()
    convert_to_csv()

if __name__ == "__main__":
    main()