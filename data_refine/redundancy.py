class ExcludeRedundancy():
    """ Exclude Redundancy data
    """
    def __init__(self):
        pass
    
    def get_result(self, data):
        """ Get Clean Data without redundency.

        :param data: DataFrame

        :return: NewDataframe output

        example
            >>> output = ExcludeRedundancy().get_result(data)
        """
        self.result = self.RemoveDuplicateData(data)
        return self.result

    def RemoveDuplicateData(self, data):
        """ Remove Duplicate Data (by column and row)

        :param data: DataFrame

        :return: NewDataframe output

        example
            >>> output = ExcludeRedundancy().RemoveDuplicateData(data)
        """
        ## Delete duplicated column, and row by index.
        # duplicated column remove
        data = data.loc[:, ~data.columns.duplicated()]
        
        # duplicated Index Drop
        data = data.sort_index()
        result = data[~data.index.duplicated(keep='first')]
        return result

 