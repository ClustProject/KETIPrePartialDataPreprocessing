import numpy as np
import pandas as pd
import sys

import json
import MeasurementOutlierDetection
import MissingPatternDetection
import Imputation


class MissingDataProcessing():
    def __init__(self, imputation_parameter):
        self.imputation_method = imputation_parameter['imputation_method']
        self.totalNanLimit = imputation_parameter['totalNanLimit']
        
    def setData(self, data):
        self.data = data
        self.totalLength = len(data)
        self.columns = data.columns
        

    def serialImputation(self):
        self.columnNaNCount={}
        self.columnNaNRatio={}
        for column in self.columns:
            self.columnNaNCount[column]=self.data[column].isna().sum()
            self.columnNaNRatio[column]=round(float(self.columnNaNCount[column]*100/self.totalLength), 2)
            if (self.columnNaNRatio[column] < self.totalNanLimit):
            # if total column NaN number is less tan limit, Impute it according to the parameter
                column_data = self.data[[column]]
                for method_set in self.imputation_method:
                     # 1. Measurement Outlier Detection Module`
                    Outlier2NaN = MeasurementOutlierDetection.OutlierDetection()
                    column_data = Outlier2NaN.certain_outlier_detection(column_data, column)
                    column_data = Outlier2NaN.uncertain_outlier_detection(column_data, column)

                    # 2. Missing Pattern Detection Module
                    NaNPatternCheck = MissingPatternDetection.MissingPatternDetection()
                    column_data = NaNPatternCheck.get_missing_pattern(column_data, column)

                    # 3. Missing Data Imputation
                    Imputer = Imputation.imputation_methods()
                    column_data = self.imputeColumnData(method_set, column_data)
                    
    def imputeColumnData(self, method_set, data):
        min_limi = method_set['min']
        max_limit = method_set['max']
        method = method_set['method']
        if method == 'mean':
            dataset = Imputer.mean_interpolate(dataset, args.column, min_limi, max_limit)

        elif method == 'median':
            dataset = Imputer.median_interpolate(dataset, args.column, min_limi, max_limit)

        elif method == 'bfill':
            dataset = Imputer.bfill(dataset, args.column, min_limi, max_limit)

        elif method == 'ffill':    
            dataset = Imputer.ffill(dataset, args.column, min_limi, max_limit)

        if method == 'linear':
            dataset = Imputer.linear_interpolate(dataset, args.column, min_limi, max_limit)
        
        elif method == 'time':
            dataset = Imputer.time_interpolation(dataset, args.column, min_limi, max_limit)

        elif method == 'nearest':
            dataset = Imputer.nearest_interpolate(dataset, args.column, min_limi, max_limit)

        elif method == 'zero':
            dataset = Imputer.zero_interpolate(dataset, args.column, min_limi, max_limit)

        elif method == 'slinear':
            dataset = Imputer.slinear_interpolate(dataset, args.column, min_limi, max_limit)

        elif method == 'quadratic':
            dataset = Imputer.quadratic_interpolate(dataset, args.column, min_limi, max_limit)

        elif method == 'cubic':
            dataset = Imputer.cubic_interpolate(dataset, args.column, min_limi, max_limit)
    
        elif method == 'spline':
            dataset = Imputer.spline_interpolate(dataset, args.column, min_limi, max_limit)

        elif method == 'barycentric':
            dataset = Imputer.barycentric_interpolate(dataset, args.column, min_limi, max_limit)

        elif method == 'polynomial':
            dataset = Imputer.polynomial_interpolate(dataset, args.column, min_limi, max_limit)
            
        
        
class getData():
    def getInfluxDB(self):
        pass
    
    def getFileInput(self, file_name, time_index="timedate"):
        dataset = pd.read_csv(file_name, parse_dates=True, index_col=[time_index])
        return dataset
    
input_file = './data_miss_original.csv'
imputation_parameter ={
   "imputation_method":[
      {
         "min":0,
         "max":1,
         "method":"mean"
      },
      {
         "min":2,
         "max":4,
         "method":"linear"
      },
      {
         "min":5,
         "max":10,
         "method":"brits"
      }
   ],
   "totalNanLimit":0.3
}

dataset = getData().getFileInput(input_file, 'timedate')
MDP = MissingDataProcessing(imputation_parameter)
MDP.setData(dataset)
MDP.serialImputation()
