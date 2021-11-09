class RefineData():
    def __init__(self):
        pass

    def makeRefineData(self, data, refine_param):
        self.refine_param = refine_param
        ### Duplication
        if refine_param['removeDuplication'] == True:
            result = self.duplicate_data_remove(data)
            print("data Length after removeDuplication:", len(result))
            self.dataWithoutDuplication = result
        else:
            self.dataWithoutDuplication = data.copy()

        ### staticFrequency
        if refine_param['staticFrequency'] == True:
            result = self.make_static_frequency(self.dataWithoutDuplication)
            print("data Length after make_static_frequency:", len(result))
            self.dataStaticFrequency = result
        else:
            self.dataStaticFrequency = self.dataWithoutDuplication.copy()
        
        self.result = self.dataStaticFrequency
        return self.result

    def duplicate_data_remove(self, data):
        ## Delete duplicated column, and row by index.
        # duplicated column remove
        data = data.loc[:, ~data.columns.duplicated()]
        # duplicated Index Drop
        data = data.sort_index()
        valid_data = data[~data.index.duplicated(keep='first')]
        #
        return valid_data

    def make_static_frequency(self, data):
        # This function makes data with static frequency.
        # If this data has a static frequency from 3 data points, 
        # make the static description time-indexed data
        estimated_frequency = self.get_frequency(data)
        if estimated_frequency:
            data_staticFrequency = data.asfreq(freq=estimated_frequency)
        else:
            data_staticFrequency = data.copy()

        return data_staticFrequency
    def get_frequency(self, data):
        if len(data)> 3:
            # Simply compare 2 intervals from 3 data points.
            # And get estimated frequency.
            inferred_freq1 = (data.index[1]-data.index[0])
            inferred_freq2 = (data.index[2]-data.index[1])
           
            if inferred_freq1 == inferred_freq2:
                estimated_freq = inferred_freq1
            else:
                estimated_freq = None
        else:
            estimated_freq = None
        return estimated_freq
