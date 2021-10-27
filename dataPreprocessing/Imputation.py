import numpy as np
import pandas as pd

# from sklearn.impute import SimpleImputer, KNNImputer, IterativeImputer
# from sklearn.experimental import enable_iterative_imputer

# temp_miss = temp_miss.assign(temp_na_mean = lambda x: SimpleImputer(strategy='mean').fit_transform(x[['temp']]),
#                                temp_na_median = lambda x: SimpleImputer(strategy='median').fit_transform(x[['temp']]),
#                                temp_na_most_frequent = lambda x: SimpleImputer(strategy='most_frequent').fit_transform(x[['temp']]),
#                                temp_na_last = lambda x: x['temp'].fillna(method='f   fill'),
#                                temp_na_next = lambda x: x['temp'].fillna(method='bfill'),
#                                temp_na_last_next = lambda x: x[['temp_na_last', 'temp_na_next']].mean(axis=1),
#                                temp_na_knn = lambda x: KNNImputer(n_neighbors=3, weights='distance').fit_transform(x[['temp']])[:, 0],
#                                temp_na_iterative = lambda x: IterativeImputer().fit_transform(x[['temp']])[:, 0],
#                                temp_na_zero = lambda x: SimpleImputer(fill_value=0.0, strategy='constant').fit_transform(x[['temp']])
#                                )


class imputation_methods():

    def __init__(self):
        pass

    def mean_interpolate(self, data, min, max):
        data.fillna(data.mean(), limit = max)
        return data
    
    def median_interpolate(self, data, min, max):
        data.fillna(data.median(), limit = max)
        return data

    def bfill(self, data, min, max):
        data.fillna(method='bfill', limit = max)
        return data

    def ffill(self, data, min, max):
        data.fillna(method='ffill', limit = max)
        return data

    def linear_interpolate(self, data, min, max):
        data.interpolate(method='linear', limit=max)
        return data

    def time_interpolation(self, data, min, max):
        data.interpolate(method = 'time', limit = max)
        return data

    def nearest_interpolate(self, data, min, max):
        data.interpolate(method='nearest', limit = max)
        return data

    def zero_interpolate(self, data, min, max):
        data.interpolate(method='zero', limit = max)
        return data

    def slinear_interpolate(self, data, min, max):
        data.interpolate(method='slinear', limit = max)
        return data

    def quadratic_interpolate(self, data, min, max):
        data.interpolate(method='quadratic', limit = max)
        return data

    def cubic_interpolate(self, data, min, max):
        data.interpolate(method='cubic', limit = max)
        return data

    def spline_interpolate(self, data, min, max, order):
        data.interpolate(method='spline', limit = max, order = order)

    def barycentric_interpolate(self, data, min, max):
        data.interpolate(method='barycentric', limit = max)
        return data

    def polynomial_interpolate(self, data, min, max, order):
        data.interpolate(method='polynomial', limit = max, order = order)
   