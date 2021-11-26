class OutlierToNaN():
    def __init__(self, outlier_param):
        self.outlier_param = outlier_param
        # Uncertain Remove 에 대한 조절 파라미터 필요 # input parameter로 받아야 함
        # 지금은 강제 True 설정 더 정교해야 Uncertain에 대해서 잘 control 가능해 보임
        self.limit_min_max = self.dataRangeInfoManager(self.outlier_param['data_type'])

    def dataRangeInfoManager(self, data_type):
        from KETIPrePartialDataPreprocessing.data_manager import dataRangeInfo_manager
        limit_min_max = dataRangeInfo_manager.MinMaxLimitValueSet().get_data_min_max_limitSet(data_type)
        return limit_min_max

    def getDataWithNaN(self, data):
        # Make Outlier to Nan according to the parameter
        # CertainOutlierToNaN == True : clean only certain outlier data.
        # UncertainOUtlierToNaN == Ture : clean uncertain outlier data.
        datawithMoreCertainNaN = self.getDataWithCertainNaN(data)
        datawithMoreUnCertainNaN = self.getDataWithUncertainNaN(datawithMoreCertainNaN)
        return datawithMoreCertainNaN, datawithMoreUnCertainNaN

    def getDataWithCertainNaN(self, data):
        if self.outlier_param['certainOutlierToNaN']['flag'] ==True:  
            from KETIPrePartialDataPreprocessing.outlier_detection import outlierRemove
            datawithMoreCertainNaN = outlierRemove.CertainOutlierRemove(data, self.limit_min_max).getDataWitoutCertainOutlier()  
            print("getDataWithCertainNaN")
        else:
            datawithMoreCertainNaN = data.copy()
        return datawithMoreCertainNaN
    
    def getDataWithUncertainNaN(self, data):    
        if self.outlier_param['uncertainOutlierToNaN']['flag'] == True:
            print("getDataWithUncertainNaN")
            from KETIPrePartialDataPreprocessing.outlier_detection import outlierRemove
            param = self.outlier_param['uncertainOutlierToNaN']['param']
            datawithMoreUnCertainNaN = outlierRemove.UnCertainOutlierRemove(data, param).get_neighbor_error_detected_data()
        else:
            datawithMoreUnCertainNaN = data.copy()
        return datawithMoreUnCertainNaN


