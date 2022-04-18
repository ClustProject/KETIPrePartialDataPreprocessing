
import warnings
warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd
from tqdm import tqdm

import sranodec as anom
from sklearn.ensemble import IsolationForest   
from sklearn.neighbors import KernelDensity, LocalOutlierFactor
from sklearn.mixture import GaussianMixture

class DataOutlier():
    def __init__(self, config, raw_data):
        """
        :param config: config 
        :type config: dictionary
        
        :param raw_data: train data whose shape is (num_index x num_variable)
        :type raw_data: dataframe
        
        example
            >>> AlgParameterEx = {
                    "IF":{
                        'percentile': percentile, # 예측시 활용되는 outlier 임계값, int or float
                        'IF_estimators': 100, # ensemble에 활용하는 모델 개수, int(default: 100, 데이터 크기에 적합하게 설정)
                        'IF_max_samples': 'auto', # 각 모델에 사용하는 샘플 개수(샘플링 적용), int or float(default: 'auto')
                        'IF_contamination': 'auto', # 모델 학습시 활용되는 데이터의 outlier 비율, ‘auto’ or float(default: ’auto’, float인 경우 0 초과, 0.5 이하로 설정)
                        'IF_max_features': 1.0, # 각 모델에 사용하는 변수 개수(샘플링 적용), int or float(default: 1.0)
                        'IF_bootstrap': False}, # bootstrap적용 여부, bool(default: False)
                    "KDE":{
                        'percentile': percentile, # 예측시 활용되는 outlier 임계값, int or float
                        'KDE_bandwidth': 0.2, # kernel의 대역폭, float(default: 1.0)
                        'KDE_algorithm': 'auto', # 사용할 tree 알고리즘, {‘kd_tree’,‘ball_tree’,‘auto’}(default: ’auto’) 중 택 1
                        'KDE_kernel': 'gaussian', # kernel 종류, {'gaussian’, ‘tophat’, ‘epanechnikov’, ‘exponential’, ‘linear’, ‘cosine’}(default: ’gaussian’) 중 택 1
                        'KDE_metric': 'euclidean', # 사용할 거리 척도, str(default: ’euclidean’)
                        'KDE_breadth_first': True, # breadth(너비) / depth(깊이) 중 우선순위 방식 정의, bool, True: breadth or False: depth
                        'KDE_leaf_size': 40}, # tree 알고리즘에서의 leaf node 개수, int(default: 40)}
                    "LOF":{
                        'percentile': percentile, # 예측시 활용되는 outlier 임계값, int or float
                        'LOF_neighbors': 5, # 가까운 이웃 개수, int(default: 20)
                        'LOF_algorithm': 'auto', # 가까운 이웃을 정의하기 위한 알고리즘, {‘auto’, ‘ball_tree’, ‘kd_tree’, ‘brute’}(default: ’auto’) 중 택 1
                        'LOF_leaf_size': 30, # tree 알고리즘에서의 leaf node 개수, int(default: 30)
                        'LOF_metric': 'minkowski'}, # 이웃을 정의하기 위한 거리 척도, str or callable(default: ’minkowski’)
                    "MoG": {# EM 방법론 반복 횟수, int(default: 100)
                        'percentile': percentile, # 예측시 활용되는 outlier 임계값, int or float
                        'MoG_components': 2, # mixture에 활용하는 component의 개수, int(default: 1)
                        'MoG_covariance': 'full', # {‘full’, ‘tied’, ‘diag’, ‘spherical’}(default: ’full’) 중 택 1
                        'MoG_max_iter': 100},
                    "SR":{
                        'percentile': percentile, # 예측시 활용되는 outlier 임계값, int or float
                        'SR_series_window_size': 24, # series window 크기, int, 데이터 크기에 적합하게 설정
                        'SR_spectral_window_size': 24, # spectral window 크기, int, 데이터 크기에 적합하게 설정
                        'SR_score_window_size': 100}# score window 크기, int, period보다 충분히 큰 size로 설정
                    }
            >>> config = { 
                    'algorithm': 'IF', # outlier detection에 활용할 알고리즘 정의, {'SR', 'LOF', 'MoG', 'KDE', 'IF'} 중 택 1            
                    'alg_parameter': AlgParameterEx['IF']      
                }
            >>> data_outlier = mod.DataOutlier(config, raw_data)
            >>> replaced_data, index_list = data_outlier.getResult()
        """

        self.algorithm = config['algorithm']
        self.args = config['alg_parameter']
        self.data = raw_data.copy()
        
    ### Outlier Detector
    def getResult(self):
        """    
        :return index_list: indices of detected outliers
        :type: json

        # Output Example
        ``` json
        {'in_co2': array([  324,  1229,  1230, ..., 50274, 50275, 50276])}
        ```
        """
        self.columns_list = list(self.data.columns)
        index_list={}
        for col in tqdm(self.data.columns):
            if self.algorithm == "SR":
                data_col = self.data[col].values
            else:
                data_col = self.data[col].values.reshape(-1, 1)
            indexes = self.getOutIndex(data_col)

            indexes = self.data[col].iloc[indexes].index
            index_list[col] = indexes
        return index_list
    
    def getOutIndex(self, data_col):
        """
        :param data_col: data for each column
        :type: np.array
        
        :return model: fitted model of selected outlier detection algorithm
        :type: model

        :return indexes: indices of detected outliers
        :type: list
        """
        if self.algorithm == 'SR':
            model = anom.Silency(self.args['SR_spectral_window_size'], self.args['SR_series_window_size'],
                                 self.args['SR_score_window_size'])
            score = model.generate_anomaly_score(data_col)
            indexes = np.where(score > np.percentile(score, self.args['percentile']))[0]
        elif self.algorithm == 'LOF':
            model = LocalOutlierFactor(n_neighbors=self.args['LOF_neighbors'], novelty=True, 
                                       algorithm=self.args['LOF_algorithm'], leaf_size=self.args['LOF_leaf_size'], 
                                       metric=self.args['LOF_metric']).fit(data_col)
            score = - 1.0 * model.score_samples(data_col)
            indexes = np.where(score > np.percentile(score, self.args['percentile']))[0]
        elif self.algorithm == 'MoG':
            model =  GaussianMixture(n_components=self.args['MoG_components'], covariance_type=self.args['MoG_covariance'], 
                                     max_iter=self.args['MoG_max_iter'], random_state=0).fit(data_col)
            score = - 1.0* model.predict_proba(data_col)
            indexes = np.where(score[:, 0] > np.percentile(score[:, 0], self.args['percentile']))[0]
        elif self.algorithm == 'KDE':
            model = KernelDensity(kernel=self.args['KDE_kernel'], bandwidth=self.args['KDE_bandwidth'], 
                                  algorithm=self.args['KDE_algorithm'], metric=self.args['KDE_metric'], 
                                  breadth_first=self.args['KDE_breadth_first'], 
                                  leaf_size=self.args['KDE_leaf_size']).fit(data_col)
            score = - 1.0 * model.score_samples(data_col)
            indexes = np.where(score > np.percentile(score, self.args['percentile']))[0]
        elif self.algorithm == 'IF':
            model = IsolationForest(n_estimators=self.args['IF_estimators'], max_samples=self.args['IF_max_samples'], 
                                    contamination=self.args['IF_contamination'], max_features=self.args['IF_max_features'], 
                                    bootstrap=self.args['IF_bootstrap']).fit(data_col)
            score = - 1.0 * model.score_samples(data_col)
            indexes = np.where(score > np.percentile(score, self.args['percentile']))[0]
        return indexes

def getMoreNaNDataByNaNIndex(data, NaNIndex):
    """
    :param data_col: data
    :type: dataFrame

    :param NaNIndex: NaNIndex
    :type: dictionary
    
    :return NaNData: data with NaN according to the NaNIndex
    :type: dataFrame
    """
    NaNData = data.copy()
    for column in data.columns:
        if column in NaNIndex.keys():
            indexes = NaNIndex[column]
            NaNData[column].loc[indexes] =np.nan 
    return NaNData

def getNaNIndex(data):
    """
    :param data_col: data
    :type: dataFrame
    
    :return NaNIndex: NaN Index of data
    :type: dictionary
    """

    NaNIndex={}
    for column in data.columns:
        NaNIndex[column]= data[data[column].isna()].index
    return NaNIndex