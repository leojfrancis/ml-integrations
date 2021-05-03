import csv
import pandas as pd
from sklearn.preprocessing import LabelEncoder


class CsvHandler:
    def __init__(self, **kwargs):
        _file = self.read_csv()
        self.LABEL_ENCODE_LIMIT = 8
        self.filePath = kwargs.get('filepath')
        self.pdFile = _file
        self.initialFile = _file
        self.colunms = self.get_colunm_keys()

    def read_csv(self, skipRows=0):
        return pd.read_csv(self.filePath, skiprows=skipRows)

    def get_colunm_keys(self):
        return list(self.pdFile.columns)

    def remove_colunm(self, toDrop):
        self.pdFile.drop(list(toDrop), axis=1, inplace=True)

    def get_col_dtypes(self):
        return [[data_type, self.pdFile.dtypes[data_type]] for data_type in self.colunms]

    def _check_label_encode(self, column):
        return self.pdFile[column].nunique() <= self.LABEL_ENCODE_LIMIT

    def label_encode_key_value(self, column):
        if self._check_label_encode(column):
            labelencoder = LabelEncoder()
            unique_elements = self.pdFile[column].unique()
            keys = labelencoder.fit_transform(unique_elements)
            zip_list = list(zip(unique_elements, keys))
            zip_list.sort(key=lambda x: x[1])
            return zip_list
        else:
            raise Exception(
                f"Cannot run label encode if number of unique values are more than {self.LABEL_ENCODE_LIMIT}")

    def run_label_encode(self, columns):
        labelencoder = LabelEncoder()
        if self._check_label_encode(column):
            for col in list(columns):
                self.pdFile[col] = labelencoder.fit_transform(self.pdFile[col])
        else:
            raise Exception(
                f"Cannot run label encode if number of unique values are more than {self.LABEL_ENCODE_LIMIT}")
