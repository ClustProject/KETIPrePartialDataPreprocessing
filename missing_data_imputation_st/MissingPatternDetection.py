import pandas as pd

class MissingPatternDetection():

    def __init__(self):
        pass

    def get_missing_pattern(self, data, column):
        # column별 missing value index 및 consecutiveness 카운팅 column 생성
        pd.concat([
            data,
            (data[column].isnull().astype(int)
            .groupby(data[column].notnull().astype(int).cumsum())
            .cumsum().to_frame('nan_count_'+column)
            )], axis=1)        
        ## data[column].isnull().astype(int).groupby(data[column].notnull().astype(int).cumsum()).cumsum
        
        return data