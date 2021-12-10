import pandas as pd

class DLImputation():
    def __init__ (self, data, method, parameter):
        self.method = method
        self.parameter = parameter
        self.data = data

    def getResult(self):
        if self.method == 'brits':
            result = self._britsImputation(self.data, self.parameter)
        else:
            result = self.data
        return result

    def _britsImputation(self, data, parameter):
        print("birts_imputation")
        column_name = data.columns[0]
        print(data)
        dataset = [data[[column_name]][i:i+1000] for i in range(0, len(data), 1000)]
        result = pd.DataFrame()
        for split_data in dataset:
            from KETIPrePartialDataPreprocessing.data_imputation.DL.brits import inference
            result_split = inference.BritsInference(split_data, parameter).get_result()
            result = pd.concat([result, result_split])
        return result

        # print("brits_training")
        # column_name = data.columns[0]
        # data_1000 = data[[column_name]][:1000]
        # from KETIPrePartialDataPreprocessing.data_imputation.DL.brits import inference
        # result = inference.BritsInference(data_1000, parameter).get_result()
        
        # split_dataset = [data[[column_name]][i:i+1000] for i in range(1000, len(data), 1000)]

        # for split_data in split_dataset:
        #     from KETIPrePartialDataPreprocessing.data_imputation.DL.brits import inference
        #     result_split = inference.BritsInference(split_data, parameter).get_result()
        #     result = pd.concat([result, result_split])
        # return result