class FrequencyRefine():
    def __init__(self, data, inferred_freq=None):
        self.data = data
        self.inferred_freq = inferred_freq
        if not self.inferred_freq:
            self.inferred_freq = self.get_frequencyWith3DataPoints(self.data)

    def get_result(self):
        self.data_staticFrequency =  self.make_static_frequency(self.data)
        return self.data_staticFrequency

    def get_inferred_freq(self):
        return self.inferred_freq

    def make_static_frequency(self, data):
        # This function makes data with static frequency.
        data_staticFrequency = data.copy()
        data_staticFrequency = data_staticFrequency.sort_index()
        data_staticFrequency = data_staticFrequency.asfreq(freq=self.inferred_freq)
        
        return data_staticFrequency
    
    def get_frequencyWith3DataPoints(self, data):
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