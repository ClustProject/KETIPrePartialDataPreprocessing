import os
from tkinter import Y

"""
self.ScikitLearnMethods =['KNN','MICE']
self.simpleMethods =['most_frequent', 'mean', 'median', ' constant']
self.fillNAMethods = ['bfill','ffill']
self.simpleIntMethods= ['linear', 'time', 'nearest', 'zero', 'slinear','quadratic', 'cubic', 'barycentric']
self.orderIntMethods = [ 'polynomial', 'spline']
self.deepMethods = ['brits']
"""

BritsModelFolder = os.path.join('c:', os.sep,'Users', 'bunny','Code_CLUST', 'KETIToolDL','DL','Models', 'brits','air_indoor_요양원', 'ICL1L2000011', 'in_ciai')
#BritsModelFolder = os.path.join("DL", "Models",'brits','air_indoor_요양원', "ICL1L2000011",'in_ciai')
refine_param = {"removeDuplication":{"flag":True}, "staticFrequency":{"flag":True, "frequency":None}}

# frequency: freqDateOffset|str|None
outlier_param  = {
    "certainErrorToNaN":{"flag":True},
    "unCertainErrorToNaN":{"flag":True,"param":{"neighbor":[0.5, 0.6]}},
    "data_type":"air"
}

imputation_param = {
"serialImputation":{
    "flag":True,
    "imputation_method":[{"min":0,"max":1,"method":"linear", "parameter":{}}, 
                            {"min":2,"max":3,"method":"brits", "parameter":{"model_address":BritsModelFolder}},
                            {"min":4,"max":100,"method":"mean", "parameter":{}}
    ],"totalNonNanRatio":80}
}

process_param = {'refine_param':refine_param, 'outlier_param':outlier_param, 'imputation_param':imputation_param}

def inputControl(inputType):
    from KETIPrePartialDataPreprocessing.dataTest.multipleSourceIngestion import getData
    dataC = getData()
    if inputType=="file":
        BASE_DIR = os.getcwd()
        input_file = os.path.join(BASE_DIR, 'sampleData', 'data_miss_original.csv')
        input_data = dataC.getFileInput(input_file, 'timedate')
    elif inputType =="influx":
        db_name  = 'air_indoor_경로당'
        ms_name = 'ICL1L2000235' 
        input_data = dataC.getInfluxInput(db_name, ms_name)

    return input_data