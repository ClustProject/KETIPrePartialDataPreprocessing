import pandas as pd
import os
from KETIToolDL import modelSetting
class DLImputation():
    def __init__ (self, data, method, parameter):
        self.method = method
        self.parameter = parameter
        self.data = data
        ####
        self.trainDataPath =parameter['trainDataPath']
        
    def getResult(self):
        result = self.data.copy()
        ### Brits
        if self.method == 'brits':
            print("brits_imputation")
            for column_name in self.data.columns:
                self.trainDataPath.append(column_name)
                from KETIToolDL.ModelTool import modelFileManager
                PathInfo = modelFileManager.setPathInfo(self.method, modelSetting, self.trainDataPath)
                modelFilePath = modelFileManager.setModelFilesName(PathInfo)
                result = britsColumnImputation(self.data[[column_name]], column_name, modelFilePath)
                result[column_name] = result
        ### Define Another Imputation 
        else:
            result = self.data
        return result

    def getModelPath(self, modelSetting, trainDataPath):
        PathInfo={}
        PathInfo['ModelRootPath'] = modelSetting.model_rootPath
        PathInfo['ModelInfoPath'] = modelSetting.modelParameterInfoList[self.method]["model_method"]
        PathInfo['TrainDataPath'] = trainDataPath
        PathInfo['ModelFileName'] = modelSetting.modelParameterInfoList[self.method]["model_fileName"]
        from KETIToolDL.ModelTool import modelFileManager
        modelFilePath = modelFileManager.setModelFilesName(PathInfo)
            
        return modelFilePath


## Define each DL imputation interface

def britsColumnImputation(data, column_name, modelPath):
    if os.path.isfile(modelPath[0]):
        from KETIToolDL.PredictionTool.Brits import inference
        n =300
        dataset = [data[[column_name]][i:i+n] for i in range(0, len(data), n)]
        result = pd.DataFrame()
        print(len(data))
        for split_data in dataset:
            print(len(split_data))
            result_split = inference.BritsInference(split_data, column_name, modelPath).get_result()
            #result_split = BritsInference(split_data, column_name).get_result()
            result = pd.concat([result, result_split])
    else:
        result = data.copy()
        print("No Brits Folder")

    return result

        
