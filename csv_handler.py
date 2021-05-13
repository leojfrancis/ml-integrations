import csv
import pandas as pd
import numpy as np
from typing import List


class CsvHandler:
    LABEL_ENCODE_LIMIT = 8

    def __init__(self, **kwargs):
        self.filePath = kwargs.get('filepath')
        _file = self.read_csv()
        self.initialData = _file
        self.pdsData = _file
        # self.preProcessData = _file
        self.colunms = self.get_colunm_keys()
        self.outColKey = self.set_out_col_index()

    def __call__(self):
        try:
            self.run_pre_processing()
        except Exception as e:
            raise e
        return e

    def __repr__(self):
        return self.filePath.split('/')[-1]

    def __len__(self):
        return self.pdsData.size

    def set_out_col_index(self, col=''):
        return col if col != '' else self.colunms[-1]

    def read_csv(self, skipRows=0):
        try:
            _file = pd.read_csv(self.filePath, skiprows=skipRows)
        except Exception as e:
            _file = e
            raise e
        return _file

    def initial_check(self, initial=False):
        return self.pdsData if not initial else self.initialData

    def get_colunm_keys(self, initial=False):
        final = self.initial_check(initial)
        return list(final.columns)

    def run_remove_colunm(self, toDrop):
        self.pdsData.drop(list(toDrop), axis=1, inplace=True)
        self.colunms = self.get_colunm_keys()

    def get_col_dtypes(self, initial=False):
        final = self.initial_check(initial)
        return [[data_type, final.dtypes[data_type]] for data_type in self.get_colunm_keys(initial)]

    def _check_label_encode(self, col: List) -> List:
        return self.initialData[col].nunique() <= self.LABEL_ENCODE_LIMIT

    def label_encode_key_value(self, col):
        if self._check_label_encode(col):
            unique_elements = self.initialData[col].unique()
            new_df = pd.DataFrame(unique_elements, columns=[
                                  'key'], dtype='category')
            new_df['value'] = new_df['key'].cat.codes
            zip_list = new_df.values.tolist()
            zip_list.sort(key=lambda x: x[1])
            return zip_list
        else:
            raise Exception(
                f"Cannot run label encode if number of unique values are more than {self.LABEL_ENCODE_LIMIT}")

    def run_label_encode(self, columns: List) -> None:
        for col in list(columns):
            if self._check_label_encode(col):
                self.pdsData[col] = self.pdsData[col].astype('category')
                self.pdsData[col] = self.pdsData[col].cat.codes
            else:
                raise Exception(
                    f"Cannot run label encode if number of unique values are more than {self.LABEL_ENCODE_LIMIT}")

    def replace_nan_values(self, col='', how='mean'):
        how = how.replace(' ', '').lower()
        try:
            describe = self.pdsData[col].describe()
        except KeyError:
            pass
        if how == 'delete':
            self.pdsData.dropna(axis=0, how='any', inplace=True)
        elif how == '75%':
            self.pdsData[col].fillna(describe[how], inplace=True)
        elif how == 'mean':
            self.pdsData[col].fillna(describe[how], inplace=True)
        elif how == 'mode':
            self.pdsData[col].fillna(self.pdsData[col].mode(), inplace=True)
        elif how == 'median':
            self.pdsData[col].fillna(self.pdsData[col].median(), inplace=True)
        elif how == 'max':
            self.pdsData[col].fillna(describe[how], inplace=True)
        else:
            raise Exception(
                f"'75%' or 'mean' or 'mode' or 'median' or 'max' or 'delete' are only accepted given {how}")

    def split_test_train(self):
        df = self.pdsData
        msk = np.random.rand(len(df)) < 0.8
        train = df[msk]
        test = df[~msk]
        print(mks)
        return[train.iloc[:, :-1], train.iloc[:, -1:], test.iloc[:, :-1], test.iloc[:, -1:]]

    def run_pre_processing(self):
        # TODO: need to make the whole preprocessing steps.
        self.pdsData.dropna(
            axis=0, how='all', inplace=True)

    def get_sample(self):
        return self.pdsData.sample(n=1)


if __name__ == "__main__":
    final = CsvHandler(
        filepath='dataset/healthcare-dataset-stroke-data.csv')
    final.run_remove_colunm(toDrop=['id', ])
    key_value = final.label_encode_key_value(col='Residence_type')
    final.replace_nan_values(how='delete')
    s = len(final)
    [num for num in final.pdsData.isnull().sum()]
    print(final.pdsData.describe(), sep='\n')
