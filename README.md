
# KETIPrePartialDataPreprocessing
> Preprocessing module for one single dataset. 

It includes cleaning, imputation, outlier detection modules.
And It also has dataRemoveByNaN module which remove a part of data according to the NaN status.

## 1. makeNaNImputationTest.py (+ makeNaNImputationTest.ipynb)
> This is the code to test the data_preprocessing module 
> Input can be both file or inlxlufDB 
(If you want to change db and measurement name, you need to modify multipleDataSourceIngestion.py)

## 2. data_preprocessing.py
### 2-1. function get_preprocessed_data(input_data, refine_param, outlier_param, imputation_param)
> This function gets cleaner data by all possible data preprocessing modules from KETIPrePartialDataPreprocessing packages.

### 2-2. DataPreprocessing (class)
> This class provdies several preprocessing Method from this package.

- So far, data refining, outlier removal, imputation module are available.
- There is a plan to expand more preprocessing modules.

### get_refinedData(self, data, refine_param)
- input: data, refine_param
1) data_refine.duplicate_data_remove: Remove duplicated data
2) data_refine.make_static_frequency: Let the original data have a static frequency
- data: datafrmae type

```json
refine_param: {'removeDuplication':True, 'staticFrequency':True}
```

### get_outlierToNaNData(self, data, outlier_param)
- outlierToNaN.OutlierToNaN:Let outliered data be.
```json
     outlier_param: {'certainOutlierToNaN':True, 'uncertainOutlierToNaN':True, 'data_type':'air'}
```

### get_imputedData(self, data, impuation_param)
- Replace missing data with substituted values according to the imputation parameter.
```json
     imputation_param : {
     "imputation_method":[
          {"min":0,"max":1,"method":"mean"},
          {"min":2,"max":4,"method":"linear"},
          {"min":5,"max":10,"method":"brits"}],
      "totalNanLimit":0.3}
```
