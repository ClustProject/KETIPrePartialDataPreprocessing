import pandas as pd
import os
from KETIToolDL import modelSetting as ms
class DLImputation():
    def __init__ (self, data, method, parameter, trainDataPath):
        self.method = method
        self.parameter = parameter
        self.data = data
        self.trainDataPath =trainDataPath
        self.ModelRootPath = ms.model_rootPath
        self.ModelFileNames = ms.modelParameterInfoList[method]['model_fileName']
        
    def getResult(self):
        result = self.data.copy()
        ### Brits
        if self.method == 'brits':
            print("brits_imputation")
            for column_name in self.data.columns:
                model_path =self.getModelPath(self.trainDataPath, column_name)
                result = britsColumnImputation(self.data[[column_name]], column_name, model_path)
                result[column_name] = result
        ### Define Another Imputation 
        else:
            result = self.data
        return result

    def getModelPath(self, trainDataPath, columnName):
        PathInfo={}
        PathInfo['ModelRootPath'] = self.ModelRootPath
        PathInfo['ModelInfoPath'] = [self.method]
        trainDataPath.append(columnName)
        PathInfo['TrainDataPath'] =trainDataPath
        model_fileNames = self.ModelFileNames

        model_folder =self.getModelFolder(PathInfo)
        model_path=[]
        for i, model_fileName in enumerate(model_fileNames):
            pathName = os.path.join(model_folder, model_fileName)
            model_path.append(pathName)
            
        return model_path

    ### Same method of Train
    def getModelFolder(self, PathInfo):
        modelFolderpath =''
        for add_folder in PathInfo['ModelRootPath']:
            modelFolderpath = os.path.join(modelFolderpath, add_folder)
        for add_folder in PathInfo['ModelInfoPath']:
            modelFolderpath = os.path.join(modelFolderpath, add_folder)
        for add_folder in PathInfo['TrainDataPath']:
            modelFolderpath = os.path.join(modelFolderpath, add_folder)
        self._checkModelFolder(modelFolderpath)

        return modelFolderpath

    ### Same method of Train
    def _checkModelFolder(self, model_path):
        if not os.path.exists(model_path):
            os.makedirs(model_path) 


## Define each DL imputation interface

def britsColumnImputation(data, column_name, modelPath):
    if os.path.isfile(modelPath[0]):
        from KETIToolDL.PredictionTool.Brits import inference
        dataset = [data[[column_name]][i:i+1000] for i in range(0, len(data), 1000)]
        print(dataset)
        print(len(dataset))
        result = pd.DataFrame()
        for split_data in dataset:
            result_split = inference.BritsInference(split_data, column_name, modelPath).get_result()
            #result_split = BritsInference(split_data, column_name).get_result()
            result = pd.concat([result, result_split])
    else:
        result = data.copy()
        print("No Brits Folder")

    return result

        
