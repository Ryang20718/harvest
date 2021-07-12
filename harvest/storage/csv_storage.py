import re
from os import listdir
from os.path import isfile, join
import pandas as pd
import datetime as dt
from typing import Tuple


"""
This module serves as a storage system for pandas dataframes in with csv files.
"""

class CSVStorage:
    """
    An extension of the basic storage that saves data in csv files.
    """

    def __init__(self, save_dir: str='data'):
        super().__init__()
        """
        Adds a directory to save data to. Loads any data that is currently in the
        directory.
        """
        self.save_dir = save_dir

        self.storage_lock.acquire()

        files = [f for f in listdir(self.save_dir) if isfile(join(self.save_dir, f))]

        for file in files:
            file_search = re.search('^([\w]+)-([\w]+).csv$', file)
            symbol, interval = file_search.group(1), file_search.group(2)
            super().store(symbol, interval, pd.read_csv(join(self.save_dir, file)))

        self.storage_lock.release()

    def store(self, symbol: str, interval: str, data: pd.DataFrame) -> None:
        """
        Stores the stock data in the storage dictionary and as a csv file.
        :symbol: a stock or crypto
        :interval: the interval between each data point, must be atleast
             1 minute
        :data: a pandas dataframe that has stock data and has a datetime 
            index
        """
        super().store(symbol, interval, data)

        if not data.empty:
            self.storage_lock.acquire()
            self.storage[symbol][interval].to_csv(self.save_dir + f'/{symbol}-{interval}.csv')
            self.storage_lock.release()

        