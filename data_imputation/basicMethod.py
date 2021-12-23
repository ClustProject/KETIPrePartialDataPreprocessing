import pandas as pd 
import numpy as np
from scipy.sparse import data

from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import SimpleImputer
from sklearn.impute import IterativeImputer
from sklearn.impute import KNNImputer

class BasicImputation():
    """ This class supports basic imputation methods.
    """
    def __init__(self, data, method, max):
        """ Set data, imputation method, max value and related values
        """
        self.method = method
        self.data = data
        self.max = max
        self.columns = data.columns
        self.index = data.index

    def makeDF(self, series_result):
        dfResult = pd.DataFrame(series_result, columns = self.columns, index = self.index)
        return dfResult

    def ScikitLearnMethod(self):
        """ Get imputed data from scikit library methods. (KNN, MICE)
        """
        data = self.data
        # TODO Extend parameter
        if self.method =='KNN':
            n_neighbors = 3
            # https://scikit-learn.org/stable/modules/generated/sklearn.impute.KNNImputer.html
            series_result = KNNImputer(n_neighbors=n_neighbors).fit_transform(data)
        elif self.method =='MICE':
            #{‘mean’, ‘median’, ‘most_frequent’, ‘constant’}, default=’mean’
            # https://scikit-learn.org/stable/modules/generated/sklearn.impute.IterativeImputer.html#sklearn-impute-iterativeimputer
            series_result = IterativeImputer(random_state=0, initial_strategy='mean', sample_posterior=True).fit_transform(data)
        else:
            series_result = data
            
        result = self.makeDF(series_result)
        return result

    def simpleMethod(self):
        """ Get imputed data from scikit SimpleImputer methods
        """
        series_result = SimpleImputer(strategy=self.method, missing_values = np.nan).fit_transform(self.data)
        result = self.makeDF(series_result)
        return result

    def fillNAMethod(self):
        """ Get imputed data from fillNA methods
        """
        result = self.data.fillna(method=self.method, limit=self.max)
        return result

    def simpleIntMethod(self):
        """ Get imputed data from simple other methods
        """
        result = self.data.interpolate(method=self.method, limit = self.max, limit_direction='both')
        return result

    def orderIntMethod(self):
        """ Get imputed data from interpolation methods
        """
        result = self.data.interpolate(method=self.method, limit = self.max, order = 2, limit_direction='both')
        return result

