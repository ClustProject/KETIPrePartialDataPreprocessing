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
    def __init__(self, feature_list, freq_min):
        """
        """
        self.feature_list = feature_list
        from datetime import timedelta
        self.resample_freq = timedelta(minutes = freq_min) 
        self.refine_param = {
            "removeDuplication":{"flag":True},
            "staticFrequency":{"flag":True, "frequency":self.resample_freq}
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

    def getMultipleCleanDataSetsByFeature(self, dataSet, NanInfoForCleanData) :
        """
        refinedDataSet, refinedDataSetName: 간단한 cleaning 진행한 데이터셋
        NaNRemovedDataSet : 품질이 좋지 않은 NaN 값을 다수 포함한 컬럼을 제거한 데이터
        ImputedDataSet: datasetNanRemove의 nan을 임의대로 interpolation한 데이터
        ImputedDataSetName: datasetNanRemove 에 대한 ms 이름


        :param dataSet: input Data to be handled
        :type dataSet: dictionary
        :param NanInfoForCleanData: selection condition
        :type NanInfoForCleanData: dictionary

        :returns: self.refinedDataSet, self.refinedDataSetName, self.NaNRemovedDataSet, self.ImputedDataSetName, self.ImputedDataSet
        :rtype: 
        """

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
            refinedData, NaNRemovedData, ImputedData, finalFlag  = self.getOneCleanDataSetByFeature(data, NanInfoForCleanData)
            for feature in self.feature_list:
                if feature in data.columns:
                    if finalFlag[feature]==-1:
                        pass
                    else: ## final_flag = 0 , 1
                        self.refinedDataSet[feature].append(refinedData[[feature]])
                        self.refinedDataSetName[feature].append(ms_name)
                        if finalFlag[feature] == 1:
                            self.NaNRemovedDataSet[feature].append(NaNRemovedData[[feature]])
                            self.ImputedDataSet[feature].append(ImputedData[[feature]])
                            self.ImputedDataSetName[feature].append(ms_name)
                    
        return self.refinedDataSet, self.refinedDataSetName, self.NaNRemovedDataSet, self.ImputedDataSetName, self.ImputedDataSet

    # getMultipleCleanDataSetsByFeature() - getOneCleanDataSetByFeature() - _getDataWithFullDuration()
    # 현재 위의 3개가 연결되어 있음

    def getOneCleanDataSetByFeature(self, data, NanInfoForCleanData) :
        """
        This function gets CleanDataSet by Feature

        :param data: input Data to be handled
        :type data: dataFrame
        :param NanInfoForCleanData:  selection condition
        :type NanInfoForCleanData: dictionary

        :returns: refinedData
        :rtype: dataframe
        :returns: NaNRemovedData
        :rtype: dataFrame
        :returns: ImputedData
        :rtype: dataFrame
        :returns: finalFlag
        :rtype: dictionary (-1: no data, 0:useless data, 1:useful data)
        """

        # start_time, end_time 문제 - 기간 설정이 고정되어 있는 이슈
        data = self._getDataWithFullDuration(data)
        refinedData, DataWithMoreNaN = self._getPreprocessedData(data)

        finalFlag = {}
        NaNRemovedData = {}
        ImputedData = {}
        DRN = data_remove_byNaN.DataRemoveByNaNStatus()
        NaNRemovedData = DRN.removeNaNData(DataWithMoreNaN, NanInfoForCleanData)
        ImputedData = NaNRemovedData.copy()
        
        for feature in self.feature_list:
            finalFlag[feature] = -1
            if (feature in data.columns) and (len(refinedData) >0): # refined_data 가 존재하고, 기존 data에 feature(column)이 속해 있을 때
                finalFlag[feature] = 0
                if feature in NaNRemovedData.columns: # NaN의 limit을 넘은 컬럼 삭제 후, 컬럼이 남아있으면
                    NaNRemovedData_feature = NaNRemovedData[[feature]]
                    finalFlag[feature] = 1
                    MDP = data_preprocessing.DataPreprocessing()
                    ImputedData[feature] = MDP.get_imputedData(NaNRemovedData_feature, self.imputation_param)
            else:
                finalFlag[feature] = -1
        
        return refinedData, NaNRemovedData, ImputedData, finalFlag

    
    def _getPreprocessedData(self, data):
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

        
    # self.query_start_time, self.query_end_time 문제 이슈
    def _getDataWithFullDuration(self, data):
        # Make Data with Full Duration [query_start_time ~ query_end_time]
        if len(data)>0:
            #2. Make Full Data(query Start ~ end) with NaN
            data.index = data.index.tz_localize(None) # 지역정보 없이 시간대만 가져오기
            new_idx = pd.date_range(start = self.query_start_time, end = (self.query_end_time- self.resample_freq), freq = self.resample_freq)
            new_data = pd.DataFrame(index= new_idx)
            new_data.index.name ='time' 
            data = new_data.join(data) # new_data에 data를 덮어쓴다
        return data