class ExcludeRedundancy():
    def __init__(self, data):
        self.data = data
    
    def get_result(self):
        self.result = self._duplicate_data_remove(self.data)
        return self.result

    def _duplicate_data_remove(self, data):
        ## Delete duplicated column, and row by index.
        # duplicated column remove
        data = data.loc[:, ~data.columns.duplicated()]
        
        # duplicated Index Drop
        data = data.sort_index()
        result = data[~data.index.duplicated(keep='first')]
        return result

 