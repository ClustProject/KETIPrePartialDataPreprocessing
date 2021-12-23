import os
"""
self.ScikitLearnMethods =['KNN','MICE']
self.simpleMethods =['most_frequent', 'mean', 'median', ' constant']
self.fillNAMethods = ['bfill','ffill']
self.simpleIntMethods= ['linear', 'time', 'nearest', 'zero', 'slinear','quadratic', 'cubic', 'barycentric']
self.orderIntMethods = [ 'polynomial', 'spline']
self.deepMethods = ['brits']

"""
model_folder = os.path.join(os.getcwd(),'data_imputation','DL','brits', 'model', 'air_indoor_경로당', 'ICL1L2000234')

refine_param = {"removeDuplication":{"flag":True}, "staticFrequency":{"flag":True, "frequency":None}}

# frequency: freqDateOffset|str|None
outlier_param  = {
    "certainOutlierToNaN":{"flag":True},
    "uncertainOutlierToNaN":{"flag":True,"param":{"neighbor":[0.5, 0.6]}},
    "data_type":"air"
}

imputation_param = {
"serialImputation":{
    "flag":True,
    "imputation_method":[{"min":0,"max":3,"method":"KNN", "parameter":{}}, 
                            #{"min":4,"max":6,"method":"brits", "parameter":{"model_address":model_folder}}
                            {"min":4,"max":6,"method":"mean", "parameter":{}}
    ],"totalNonNanRatio":80}
}

process_param = {'refine_param':refine_param, 'outlier_param':outlier_param, 'imputation_param':imputation_param}