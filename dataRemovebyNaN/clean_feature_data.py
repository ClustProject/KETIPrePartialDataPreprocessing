import sys
sys.path.append("../")
sys.path.append("../..")
import pandas as pd
from KETIPrePartialDataPreprocessing.dataRemovebyNaN import data_remove_byNaN
from KETIPrePartialDataPreprocessing import data_preprocessing

# 특정 datasetd에 대해 품질을 점검하고 각 피쳐별로 이상 수치를 넘는 피쳐 데이터는 제거하고 깨끗한 데이터를 전달
# - multiple dataFrame:getMultipleCleanDataSetsByFeature
# - one dataFrame: getOneCleanDataSetByFeature

class CleanFeatureData:
    def __init__(self, feature_list, resample_freq):
        self.feature_list = feature_list
        self.resample_freq = resample_freq
        self.refine_param = {
            "removeDuplication":{"flag":True},
            "staticFrequency":{"flag":True, "frequency":resample_freq}
        }
        self.outlier_param  = {
            "certainErrorToNaN":{"flag":True},
            "unCertainErrorToNaN":{
                "flag":False,
                "param":{"neighbor": 0.5}
            },
            "data_type":"air"
        }
        self.imputation_param = {
            "serialImputation":{
                "flag":True,
                "imputation_method":[{"min":0,"max":15,"method":"linear" , "parameter":{}}],
                "totalNonNanRatio":70
            }
        }
        
    def setDataDuration(self, query_start_time, query_end_time):
        self.query_start_time = query_start_time
        self.query_end_time = query_end_time

    
    def getDataWithFullDuration(self, data):
        # Make Data with Full Duration (query_start_time - to - query_end_time)
        if len(data)>0:
            #2. Make Full Data(query Start ~ end) with NaN
            data.index = data.index.tz_localize(None)
            new_idx = pd.date_range(start = self.query_start_time, end = (self.query_end_time- self.resample_freq), freq = self.resample_freq)
            new_data = pd.DataFrame(index= new_idx)
            new_data.index.name ='time' 
            data = new_data.join(data) 
        return data

    def getPreprocessedData(self, data):
        """
        This function produced cleaner data with parameter

        :param data: input Data to be handled
        :type data: dataFrame with only one feature

        :returns: refinedData
        :rtype: dataFrame

        :returns: dataWithMoreNaN
        :rtype: dataFrame
        """
        refined_data = pd.DataFrame()
        datawithMoreUnCertainNaN = pd.DataFrame()
        if len(data)>0:
            #1. Preprocessing (Data Refining/Static Frequency/OutlierDetection)
            MDP = data_preprocessing.DataPreprocessing()
            refined_data = MDP.get_refinedData(data, self.refine_param)
            datawithMoreCertainNaN, datawithMoreUnCertainNaN = MDP.get_errorToNaNData(refined_data, self.outlier_param)
            data = datawithMoreUnCertainNaN

        return refined_data, datawithMoreUnCertainNaN

        
    def getNaNRemovedData(self, data,NanInfoForClenData):
        NaNRemovedData = None
        DRN = data_remove_byNaN.DataRemoveByNaNStatus()
        NaNRemovedData = DRN.removeNaNData(data, NanInfoForClenData)
        return NaNRemovedData

    
    def getDataByQuality(self, data, NanInfoForClenData):
        """
        This function selects only data that meet the conditions(NaNInfoForCleanData)

        :param data: input Data to be handled
        :type data: dataFrame with only one feature
        :param NanInfoForClenData:  selection condition
        :type NanInfoForClenData: dictionary

        :returns: NaNRemovedData
        :rtype: data removed NaN data

        :returns: ImputedData
        :rtype: data with imputed values

        :returns: finalFlag
        :rtype: -1: no data, 0:useless data, 1:useful data
        """
        # finalFlag -1, no data
        # finalFlag  0, useless data
        # finalFlag  1, useful data with good quality
        NaNRemovedData = pd.DataFrame()
        ImputedData = pd.DataFrame()
        if len(data) > 0:
            NaNRemovedData = self.getNaNRemovedData(data, NanInfoForClenData)
            for feature in data.columns:
                if feature in NaNRemovedData.columns:
                    finalFlag = 1 #Data: Yes, Quality: Yes
                    MDP = data_preprocessing.DataPreprocessing()
                    ImputedData = MDP.get_imputedData(data, self.imputation_param)
                else:
                    finalFlag=0       
        else:
            finalFlag = -1    #Data: No
            
        return NaNRemovedData, ImputedData, finalFlag
    
    def getMultipleCleanDataSetsByFeature(self, dataSet, NanInfoForClenData) :
        self.refinedDataSet={}
        self.refinedDataSetName={}
        self.NaNRemovedDataSet={}
        self.ImputedDataSet = {}
        self.ImputedDataSetName={}
        for feature in self.feature_list:
            self.refinedDataSet[feature]=[]
            self.refinedDataSetName[feature]=[]
            self.NaNRemovedDataSet[feature]=[]
            self.ImputedDataSet[feature] = []
            self.ImputedDataSetName[feature]=[]

        ms_list = dataSet.keys()
        for ms_name in ms_list:
            print("=======",ms_name,"=======")
            data = dataSet[ms_name]
            refinedData, NaNRemovedData, ImputedData, finalFlag  = self.getOneCleanDataSetByFeature(data, NanInfoForClenData)
            for feature in self.feature_list:
                if feature in data.columns:
                    if finalFlag[feature]==-1:
                        pass
                    else: ## final_flag = 0 , 1
                        self.refinedDataSet[feature].append(refinedData[[feature]])
                        self.refinedDataSetName[feature].append(ms_name)
                        if finalFlag[feature] == 1:
                            self.NaNRemovedDataSet[feature].append(NaNRemovedData[feature])
                            self.ImputedDataSet[feature].append(ImputedData[feature])
                            self.ImputedDataSetName[feature].append(ms_name)
                        
        """
        refinedDataSet, refinedDataSetName: 간단한 cleaning 진행한 데이터셋
        NaNRemovedDataSet : 품질이 좋지 않은 NaN 값을 다수 포함한 컬럼을 제거한 데이터
        ImputedDataSet: datasetNanRemove의 nan을 임의대로 interpolation한 데이터
        ImputedDataSetName: datasetNanRemove 에 대한 ms 이름
        """ 
        return self.refinedDataSet, self.refinedDataSetName, self.NaNRemovedDataSet, self.ImputedDataSetName, self.ImputedDataSet

    
    def getOneCleanDataSetByFeature(self, data, NanInfoForClenData) :
        """
        This function gets CleanDataSet by Feature

        :param data: input Data to be handled
        :type data: dataFrame
        :param NanInfoForClenData:  selection condition
        :type NanInfoForClenData: dictionary

        :returns: refinedData
        :rtype: dataframe

        :returns: NaNRemovedData
        :rtype: dictionary with dataFrame

        :returns: ImputedData
        :rtype: dictionary with dataFrame

        :returns: finalFlag
        :rtype: -1: no data, 0:useless data, 1:useful data
        """

        data = self.getDataWithFullDuration(data)
        refinedData, DataWithMoreNaN = self.getPreprocessedData(data)

        finalFlag = {}
        NaNRemovedData = {}
        ImputedData = {}
        for feature in self.feature_list:
            if feature in data.columns:
                NaNRemovedData[feature], ImputedData[feature], finalFlag[feature] = self.getDataByQuality(DataWithMoreNaN[[feature]], NanInfoForClenData)
            else:
                NaNRemovedData[feature]=None
                ImputedData[feature] = None
                finalFlag[feature] = -1
        return refinedData, NaNRemovedData, ImputedData, finalFlag

