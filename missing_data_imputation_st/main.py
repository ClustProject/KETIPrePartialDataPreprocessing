

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
