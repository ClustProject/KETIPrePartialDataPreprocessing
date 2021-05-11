class MinMaxLmitValueSet():
    
    def __init__(self, type):
        self.type = type
        pass

    def get_data_min_max_limitSet(self):
        if self.type =='air':
            #data_clean_partial =  edd.extream_error_deletion(data_raw_partial)
            data_min_max_limit = {'max_num':{'CO2ppm':10000, 'H2Sppm':100, 'NH3ppm':300, 'OptimalTemperature':45, 
                                       'RichTemperature':45, 'RichHumidity':100, 'comp_temp':45, 'comp_humid':100,
                                       '2ndPanSpeed':200, 'UpperPanSpeed':200,
                                      'out_humid':100,'out_pressure':2000,'out_temp':50 },
                           'min_num':{'CO2ppm':0, 'H2Sppm':0, 'NH3ppm':0, 'OptimalTemperature':-20, 'RichTemperature':-20, 
                                      'RichHumidity':0, 'comp_temp':-20, 'comp_humid':0, '2ndPanSpeed':0, 'UpperPanSpeed':0,
                                     'out_humid':0, 'out_pressure':0, 'out_temp':-30}}
            
        return data_min_max_limit