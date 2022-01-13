import pandas as pd
import os
class DLImputation():
    def __init__ (self, data, method, parameter):
        self.method = method
        self.parameter = parameter
        self.data = data

    def getResult(self):
        result = self.data.copy()

        ### Brits
        if self.method == 'brits':
            print("birts_imputation")
            for column_name in self.data.columns:
               result = britsColumnImputation(self.data[[column_name]], self.parameter, column_name)
               result[column_name] = result
               
        ### Define Another Imputation 
        else:
            result = self.data
        return result

    
def britsColumnImputation(data, parameter, column_name):
    model_address = parameter['model_address']
    if os.path.isdir(model_address):
        from KETIToolDL.imputation.brits import inference
        dataset = [data[[column_name]][i:i+1000] for i in range(0, len(data), 1000)]
        result = pd.DataFrame()
        for split_data in dataset:
            result_split = inference.BritsInference(split_data, model_address, column_name).get_result()
            result = pd.concat([result, result_split])
    else:
        result = data.copy()
        print("No Brits Folder")

    return result