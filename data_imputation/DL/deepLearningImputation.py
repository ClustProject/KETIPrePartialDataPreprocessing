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
        print("brits_training")
        from KETIPrePartialDataPreprocessing.data_imputation.DL.brits import inference
        result = inference.BritsInference(data, parameter).get_result()
        return result