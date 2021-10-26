
##
#  input: data
#
# 1. Measurement Outlier Detection

# 1-1. Certain Outlier (auto)
#
# OutlierDetection.py
# certain_outlier_detection(data, column)

# 1-2. Uncertain Outlier (select)
#
# OutlierDetection.py
# uncertain_outlier_detection(data, column)

# output: data'
##


##
# input: data'
# user input: 
# {"ConsecutiveNanLimit":
# {"method1": {"min": 0, "max": 1, "method": "mean"},
# "method2": {"min": 2, "max": 4, "method": "linear"},
# "method3": {"min": 5, "max": 10, "method": "brits"}},
# "TotalNanLimit: 0.3"}

# 2. Missing Data Pattern Check
# MissingPatternDetection.py
# 
# get_missing_pattern(data, column):

# output: data, missing index, consecutiveness
##


##
# input: data, missing pattern, parameters
# 
# 3. Missing Data Imputation
#
# imputation.py
#
# output: imputated_data
##


import numpy as np
import pandas as pd
import sys

import argparse
import json
import MeasurementOutlierDetection
import MissingPatternDetection
import Imputation


parser = argparse.ArgumentParser(description='Partial Imputation')
#   parser.add_argument('ConsecutiveNanLimit')
parser.add_argument('--input_path', type = str, default = './data_miss_original.csv', help = 'Input data path')
parser.add_argument('--column', type = str, help = 'Column to imputate')
parser.add_argument('--method1', type = str, default = 'mean', help = 'Imputation strategies for short term missing values. [mean, median, bfill, ffill]')
parser.add_argument('--method1_min', type = int, default = 0, help = 'Short term minimum length')
parser.add_argument('--method1_max', type = int, default = 1, help = 'Short term maximum length')
parser.add_argument('--method2', type = str, default = 'linear', help = 'Imputation strategies for mid term missing values. [linear, time, nearest, zero, slinear. quadratic, cubic, spline, barycentric, polynomial]')
parser.add_argument('--method2_min', type = int, default = 2, help = 'Mid term minimum length')
parser.add_argument('--method2_max', type = int, default = 5, help = 'Mid term maximum length')
parser.add_argument('--method3', type = str, default = 'brits', help = 'Imputation strategies for long term missing values. [brits, naomi, ...]')
parser.add_argument('--method3_min', type = int, default = 6, help = 'Long term mimimum length')
parser.add_argument('--method3_max', type = int, default = 10, help = 'Long term maximum length')   
parser.add_argument('--TotalNaNLimit', type = float, default = 0.3, help = 'TotalNaNLimit')
parser.add_argument('--output_path', type = str, default = './output/imputed_dataset.csv', help = ' Output destination')

def main(args):
    dataset = pd.read_csv(args.input_path)
#    dataset.set_index('timedate', inplace=True)

    total_index_num = dataset.shape[0]*(dataset.shape[1]-1) # Datetime 제외
    
    if (dataset.isnull().sum().sum())/total_index_num > args.TotalNaNLimit: # 전체 column에 대한 TotalNaNLimit
        imputed_dataset = dataset

    elif dataset[args.column].isnull().sum()/len(dataset) > args.TotalNaNLimit: # 특정 column에 대한 TotalNaNLimit
        imputed_dataset = dataset[args.column]

    else:
        # 1. Measurement Outlier Detection Module`
        Outlier2NaN = MeasurementOutlierDetection.OutlierDetection()
        dataset = Outlier2NaN.certain_outlier_detection(dataset, args.column)
        dataset = Outlier2NaN.uncertain_outlier_detection(dataset, args.column)


        # 2. Missing Pattern Detection Module
        NaNPatternCheck = MissingPatternDetection.MissingPatternDetection()
        dataset = NaNPatternCheck.get_missing_pattern(dataset, args.column)


        # 3. Missing Data Imputation
        Imputer = Imputation.imputation_methods()


        ## 3-1. method 1

        if args.method1 == 'mean':
            dataset = Imputer.mean_interpolate(dataset, args.column, args.method1_min, args.method1_max)

        elif args.method1 == 'median':
            dataset = Imputer.median_interpolate(dataset, args.column, args.method1_min, args.method1_max)

        elif args.method1 == 'bfill':
            dataset = Imputer.bfill(dataset, args.column, args.method1_min, args.method1_max)

        elif args.method1 == 'ffill':    
            dataset = Imputer.ffill(dataset, args.column, args.method1_min, args.method1_max)

        ## 3-2. method 2

        if args.method2 == 'linear':
            dataset = Imputer.linear_interpolate(dataset, args.column, args.method2_min, args.method2_max)
        
        elif args.method2 == 'time':
            dataset = Imputer.time_interpolation(dataset, args.column, args.method2_min, args.method2_max)

        elif args.method2 == 'nearest':
            dataset = Imputer.nearest_interpolate(dataset, args.column, args.method2_min, args.method2_max)

        elif args.method2 == 'zero':
            dataset = Imputer.zero_interpolate(dataset, args.column, args.method2_min, args.method2_max)

        elif args.method2 == 'slinear':
            dataset = Imputer.slinear_interpolate(dataset, args.column, args.method2_min, args.method2_max)

        elif args.method2 == 'quadratic':
            dataset = Imputer.quadratic_interpolate(dataset, args.column, args.method2_min, args.method2_max)

        elif args.method2 == 'cubic':
            dataset = Imputer.cubic_interpolate(dataset, args.column, args.method2_min, args.method2_max)
    
        elif args.method2 == 'spline':
            dataset = Imputer.spline_interpolate(dataset, args.column, args.method2_min, args.method2_max)

        elif args.method2 == 'barycentric':
            dataset = Imputer.barycentric_interpolate(dataset, args.column, args.method2_min, args.method2_max)

        elif args.method2 == 'polynomial':
            dataset = Imputer.polynomial_interpolate(dataset, args.column, args.method2_min, args.method2_max)
        
        
        ## 3-3. method 3

        # if args.method3 == 'linear':
        #     dataset = Imputer.linear_interpolate(dataset, args.column, args.method2_min, args.method2_max)
        
        # elif args.method2 == 'time':
        #     dataset = Imputer.time_interpolation(dataset, args.column, args.method2_min, args.method2_max)

        # elif args.method2 == 'nearest':
        #     dataset = Imputer.nearest_interpolate(dataset, args.column, args.method2_min, args.method2_max)

        # elif args.method2 == 'zero':
        #     dataset = Imputer.zero_interpolate(dataset, args.column, args.method2_min, args.method2_max)

        # elif args.method2 == 'slinear':
        #     dataset = Imputer.slinear_interpolate(dataset, args.column, args.method2_min, args.method2_max)

        # elif args.method2 == 'quadratic':
        #     dataset = Imputer.quadratic_interpolate(dataset, args.column, args.method2_min, args.method2_max)



    imputed_dataset.to_csv(args.output_path, index=False)

if __name__ == '__main__':
    args = parser.parse_args()
    main(args)