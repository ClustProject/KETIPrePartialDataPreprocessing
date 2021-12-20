class FrequencyRefine():
    """ Refine Data with the static frequency
    """
    def __init__(self):
        pass

    def get_RefinedData(self, data, freq=None):
        """ This function makes new data with the static description frequency according to the freq parameter status. 

        :param data: DataFrame
        :param freq: [None| DateOffset or str] Frequency of refined output data. If None, this class infers the data frequency and redefines it. 
        
        :return: NewDataframe output
        
        example
            >>> output = FrequencyRefine().get_RefinedData(data, None)

        

        """
        self.data = data
        self.freq = freq
        if not self.freq:
            self.output, self.freq = self.get_RefinedDatawithInferredFreq(data)
        else:
            self.output = self.get_RefinedDatawithStaticFreq(data, self.freq)
        return self.output

    def get_RefinedDatawithInferredFreq(self, data):
        """ This function generates data with inferred static inference frequency.

        :param data: DataFrame

        :return: NewDataframe output, inferred_frequency

        example
            >>> output, new_frequency = FrequencyRefine().get_RefinedDatawithInferredFreq(data)
        """
        
        inffered_freq = self.get_frequencyWith3DataPoints(data)
        self.output = self.make_static_frequency(data, inffered_freq)
        return self.output, inffered_freq
    
    def get_RefinedDatawithStaticFreq(self, data, freq):
        """ This function generates data with the static inference frequency.

        :param data: DataFrame
        :param freq: frequency of data to be newly 
        
        :return: NewDataframe output

        example
            >>> output = FrequencyRefine().get_RefinedDatawithStaticFreq(data, '30S')
        """
        self.output = self.make_static_frequency(data, freq)
        return self.output

    def make_static_frequency(self, data, freq):
        """ This function makes data with static frequency.

        :param data: DataFrame
        :param freq: frequency of data to be newly generated

        :return: NewDataframe output

        example
            >>> output = FrequencyRefine().make_static_frequency(data, '30S')
        """
        data_staticFrequency = data.copy()
        data_staticFrequency = data_staticFrequency.sort_index()
        data_staticFrequency = data_staticFrequency.asfreq(freq=freq)
        
        return data_staticFrequency
    
    def get_frequencyWith3DataPoints(self, data):
        """ this function finds inferred frequency of input data

        :param data: [datafrmae]

        :return: estimated_freq

        example
            >>> estimated_freq  = FrequencyRefine().get_frequencyWith3DataPoints(data)
        
        """
        if len(data)> 3:
            # Simply compare 2 intervals from 3 data points.
            # And get estimated frequency.
            inferred_freq1 = (data.index[1]-data.index[0])
            inferred_freq2 = (data.index[2]-data.index[1])
           
            if inferred_freq1 == inferred_freq2:
                estimated_freq = inferred_freq1
            else:
                inferred_freq1 = (data.index[-1]-data.index[-2])
                inferred_freq2 = (data.index[-2]-data.index[-3])
                if inferred_freq1 == inferred_freq2:
                    estimated_freq = inferred_freq1
                else :
                    estimated_freq = None
        else:
            estimated_freq = None
        
        ### None 일 경우에 그래도 estimated frequency가 나오도록만 해놨음 TODO
        if not estimated_freq:
            estimated_freq = (data.index[1]-data.index[0])

        return estimated_freq