import csv
import pandas as pd


class CsvHandler:
    def __init__(self, **kwargs):
        self.filePath = kwargs.get('filepath')
        self.pdFile = self.read_csv()
        self.colunms = self.get_colunm_keys()

    def read_csv(self, skipRows=0):
        return pd.read_csv(self.filePath, skiprows=skipRows)

    def get_colunm_keys(self):
        return list(self.pdFile.columns)
    
    def remove_colunm(self,toDrop):
        self.pdFile.drop(list(toDrop), axis = 1, inplace = True)
    
