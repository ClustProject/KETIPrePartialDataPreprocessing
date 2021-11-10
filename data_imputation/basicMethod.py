import pandas as pd 
import numpy as np

from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import SimpleImputer
from sklearn.impute import IterativeImputer
from sklearn.impute import KNNImputer

def ScikitLearnMethod(data, method, max):
    if method =='KNN':
        n_neighbors = 3
        # https://scikit-learn.org/stable/modules/generated/sklearn.impute.KNNImputer.html
        imputer = KNNImputer(n_neighbors=n_neighbors)
        series_result = imputer.fit_transform(data)
    elif method =='MICE':
        #{‘mean’, ‘median’, ‘most_frequent’, ‘constant’}, default=’mean’
        # https://scikit-learn.org/stable/modules/generated/sklearn.impute.IterativeImputer.html#sklearn-impute-iterativeimputer
        imputer = IterativeImputer(random_state=0, initial_strategy='mean', sample_posterior=True)
        series_result = imputer.fit_transform(data)
    else:
        series_result = data

    return series_result

def simpleMethod(data, method, max):
    result = SimpleImputer(strategy=method, missing_values = np.nan).fit_transform(data)
    return result

def fillNAMethod(data, method, max):
    result = data.fillna(method=method, limit=max)
    return result

def simpleIntMethod(data, method, max):
    result = data.interpolate(method=method, limit = max, limit_direction='both')
    return result

def orderIntMethod(data, method, max):
    result = data.interpolate(method=method, limit = max, order = 2, limit_direction='both')
    return result

"""
class PandasSimpleImputer(SimpleImputer):
    def __init__(self, strategy, missing_values):
        super().__init__(strategy = strategy, missing_values = missing_values)
    def fit(self, X, y=None):
        self.columns = X.columns
        self.index = X.index
        return super().fit(X, y)
    def transform(self, X):
        return pd.DataFrame(super().transform(X), columns = self.columns, index = self.index)
"""