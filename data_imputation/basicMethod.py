import pandas as pd 
import numpy as np

from sklearn.impute import SimpleImputer

# simpleMethods =['most_frequent', 'mean', 'median', 'constant']
# fillNAMethods = ['bfill','ffill']
# simpleIntMethods= ['linear', 'time', 'nearest', 'zero', 'slinear','quadratic', 'cubic', 'barycentric']
# orderIntMethods = [  'polynomial', 'spline']


class PandasSimpleImputer(SimpleImputer):
    def __init__(self, strategy, missing_values):
        super().__init__(strategy = strategy, missing_values = missing_values)

    def fit(self, X, y=None):
        self.columns = X.columns
        self.index = X.index
        return super().fit(X, y)
    def transform(self, X):
        return pd.DataFrame(super().transform(X), columns = self.columns, index = self.index)

def simpleMethod(data, method, max):
    print(method)
    data = PandasSimpleImputer(strategy=method, missing_values = np.nan).fit_transform(data)
    return data

def fillNAMethods(data, method, max):
    result = data.fillna(method=method, limit=max)
    return result

def simpleIntMethod(data, method, max):
    result = data.interpolate(method=method, limit = max, limit_direction='both')
    return result

def orderIntMethod(data, method, max):
    result = data.interpolate(method=method, limit = max, order = 2, limit_direction='both')
    return result

