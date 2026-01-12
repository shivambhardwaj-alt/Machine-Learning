import pandas as pd
import seaborn as sns
import matplotlib.pyplot as  plt
import numpy as np
from src.logger import logging
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import RobustScaler
from sklearn.impute import SimpleImputer
from src.exception import CustomException
class FeatureEngineering:
    def __init__(self,train_df:pd.DataFrame,test_df : pd.DataFrame,store_df:pd.DataFrame):
        self.train_df = train_df
        self.test_df = test_df
        self.store_df = store_df
    def handle_missing_data(self):
        try:
            logging.info('Handle Missing Values')
            self.df.fillna(self.df.mean(),inplace  = True)
            logging.info('Missing Values handled')
        except Exception as e:
            logging.error(f'Error in handing the data',{str(e)})
            raise CustomException(f'Error handling in missing data',{str(e)})
    def imputing_the_data(self,cols):
        imputer =  SimpleImputer(strategy='median')
        self.df[cols] = imputer.fit_transform(self.df[cols])
        self.df[cols] = self.df[cols].replace([np.inf,-np.inf],np.nan)



    def encode_categorical_columns(self):
        try:
            logging.info('Encode Categorical Columns')
            le = LabelEncoder()
            self.df['StoreType'] = le.fit_transform(self.df['StoreType'])
            self.df['Assortment'] = le.fit_transform(self.df['Assortment'])
            self.df['StateHoliday'] = le.fit_transform(self.df['StateHoliday'])


        except Exception as e:
            logging.error(f'Error in encoding numerical data',{str(e)})
            raise CustomException(f'Error handling in encoding of the data',{str(e)})
        
    def scale_numerical_cols(self):
        cols_to_scale = ['Sales', 'Customers', 'Open', 'CompetitionDistance','AverageCustomers','Average_Sales']
        self.imputing_the_data(cols_to_scale)
        scaler = RobustScaler()
        self.df[cols_to_scale] = scaler.fit_transform(self.df[cols_to_scale])
    #a operation is left that is merging the dataset 
    def merge_dataset(self):
        self.store_df = self.store_df.drop(['CompetitionOpenSinceMonth', 'CompetitionOpenSinceYear','Promo2SinceWeek',
                     'Promo2SinceYear', 'PromoInterval'], axis=1)
        median_competition_distance = self.store_df['CompetitionDistance'].median()
        self.store_df['CompetitionDistance'].fillna(median_competition_distance, inplace=True)
        logging.info("Extracting some features from the date object")
        self.train_df['Year'] = self.train_df['Date'].dt.year
        self.train_df['Month'] = self.train_df['Date'].dt.month
        self.train_df['Day'] =  self.train_df['Date'].dt.day
        self.train_df['WeekOfYear'] = self.train_df['train'].dt.isocalendar().week
        self.train_df['DayOfWeek'] = self.train_df['Date'].dt.dayofweek

        logging.info("Feature Extraction completed")

    def perform_feature_engineering(self):
        try:
            logging.info('FeatureEngineering has been started')
            self.handle_missing_data()
            self.encode_categorical_columns()
            self.scale_numerical_cols()
            logging.info('Feature Engineering completed Successfully!')
            return self.df
        except Exception as e : 
            logging.error(f'Error in feature engineering process: {str(e)}')
            raise CustomException(f'Error in feature engineering process: {str(e)}')


        


    
    
