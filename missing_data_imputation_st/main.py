

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

import argparse
import json
import imputation


parser = argparse.ArgumentParser(description='Partial Imputation')
#   parser.add_argument('ConsecutiveNanLimit')
parser.add_argument('--input_path', type = str, default = './data_miss.csv', help = 'Input data path')
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
parser.add_argument('--TotalNanLimit', type = float, default = 0.3, help = 'TotalNanLimit')
parser.add_argument('--output_path', type = str, default = './', help = ' Output destination')

def main(args):
    dataset = pd.read_csv(args.input_path)
    if (dataset.isnull().sum())/len(dataset) > args.TotalNaNLimit:
        return dataset
    else:
        
        imputer = imputation.imputation_methods



if __name__ == '__main__':
    args = parser.parse_args()
    main(args)