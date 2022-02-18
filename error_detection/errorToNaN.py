class errorToNaN():
    def __init__(self, outlier_param):
        self.outlier_param = outlier_param
        # Uncertain Remove 에 대한 조절 파라미터 필요 # input parameter로 받아야 함
        # 지금은 강제 True 설정 더 정교해야 Uncertain에 대해서 잘 control 가능해 보임

        # dataRangeInfoManager 대신에 limit_min_max 값을  outlier_param의 값으로 받아들이도록 수정해야 함.
        self.limit_min_max = self.dataRangeInfoManager(self.outlier_param['data_type'])

    def dataRangeInfoManager(self, data_type):
        from KETIPrePartialDataPreprocessing.dataTest import dataRangeInfo_manager
        limit_min_max = dataRangeInfo_manager.MinMaxLimitValueSet().get_data_min_max_limitSet(data_type)
        return limit_min_max

    def getDataWithNaN(self, data):
        # Make Outlier to Nan according to the parameter
        # certainErrorToNaN == True : clean only certain outlier data.
        # unCertainErrorToNaN == Ture : clean uncertain outlier data.
        datawithMoreCertainNaN = self.getDataWithCertainNaN(data)
        datawithMoreUnCertainNaN = self.getDataWithUncertainNaN(datawithMoreCertainNaN)
        return datawithMoreCertainNaN, datawithMoreUnCertainNaN

    def getDataWithCertainNaN(self, data):
        if self.outlier_param['certainErrorToNaN']['flag'] ==True:  
            from KETIPrePartialDataPreprocessing.error_detection import certainError
            anomal_value_list=[99.9, 199.9, 299.9, 9999, -99.9, -199.9, -299.9, -9999] 
            datawithMoreCertainNaN = certainError.CertainErrorRemove(data, self.limit_min_max, anomal_value_list).getDataWitoutcertainError()  
            print("getDataWithCertainNaN")
        else:
            datawithMoreCertainNaN = data.copy()
        return datawithMoreCertainNaN
    
    def getDataWithUncertainNaN(self, data):    
        if self.outlier_param['unCertainErrorToNaN']['flag'] == True:
            print("getDataWithUncertainNaN")
            from KETIPrePartialDataPreprocessing.error_detection import unCertainError
            param = self.outlier_param['unCertainErrorToNaN']['param']
            datawithMoreUnCertainNaN = unCertainError.unCertainErrorRemove(data, param).get_neighbor_error_detected_data()
        else:
            datawithMoreUnCertainNaN = data.copy()
        return datawithMoreUnCertainNaN


