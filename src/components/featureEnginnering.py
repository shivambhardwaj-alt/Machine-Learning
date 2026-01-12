import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from src.logger import logging
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import RobustScaler
from sklearn.impute import SimpleImputer
from src.exception import CustomException

class FeatureEngineering:
    def __init__(self, train_df: pd.DataFrame, test_df: pd.DataFrame, store_df: pd.DataFrame):
        self.train_df = train_df
        self.test_df = test_df
        self.store_df = store_df

        self.imputer = SimpleImputer(strategy="median")
        self.scaler = RobustScaler()
        self.label_encoders = {}

    def handle_missing_values(self, df, cols, fit=False):
        """Handle missing values by imputing with the median."""
        if fit:
            df[cols] = self.imputer.fit_transform(df[cols])
        else:
            df[cols] = self.imputer.transform(df[cols])
        df[cols] = df[cols].replace([np.inf, -np.inf], np.nan)
        return df

    def merge_dataset(self, df):
        """Merge store dataset with the main dataframe on the 'Store' column."""
        store = self.store_df.drop(['CompetitionOpenSinceMonth', 'CompetitionOpenSinceYear',
                                     'Promo2SinceWeek', 'Promo2SinceYear', 'PromoInterval'], axis=1)

       
        store['CompetitionDistance'].fillna(store['CompetitionDistance'].median(), inplace=True)

        return df.merge(store, on='Store', how='left')

    def extract_features(self, df):
        """Extract date-based features like Year, Month, Day, etc."""
        df['Date'] = pd.to_datetime(df['Date'])
        df['Year'] = df['Date'].dt.year
        df['Month'] = df['Date'].dt.month
        df['Day'] = df['Date'].dt.day
        df['WeekOfYear'] = df['Date'].dt.isocalendar().week.astype(int)
        df['DayOfWeek'] = df['Date'].dt.dayofweek
        return df

    def encode_categorical_columns(self, df, cols, fit=False):
        """Encode categorical columns using LabelEncoder."""
        for col in cols:
            if fit:
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col].astype(str))
                self.label_encoders[col] = le  
            else:
                df[col] = self.label_encoders[col].transform(df[col].astype(str))  
        return df

    def scale_numerical_columns(self, df, cols, fit=False):
        """Scale numerical columns using RobustScaler."""
        if fit:
            df[cols] = self.scaler.fit_transform(df[cols])
        else:
            df[cols] = self.scaler.transform(df[cols])
        return df

    def perform_feature_engineering(self):
        try:
            logging.info('Feature Engineering has been started')
            logging.info(f'Columns in dataset train are : ',{self.train_df.columns})
            logging.info(f'Columns in the dataset test are : ',{self.test_df.columns})
            return 
        

            if 'Sales' not in self.train_df.columns or 'Customers' not in self.train_df.columns:
                raise CustomException("Columns ['Sales', 'Customers'] are missing in the DataFrame")

            
            num_cols = ['Sales', 'Customers', 'CompetitionDistance']
            cat_cols = ['StoreType', 'Assortment', 'StateHoliday']

            # ---------------------- TRAIN --------------------------#
            train = self.merge_dataset(self.train_df)
            logging.info(f'Columns in the merged Dataset are : ',{train.columns})
            train = self.extract_features(train)
            train = self.handle_missing_values(train, num_cols, fit=True)
            train = self.encode_categorical_columns(train, cat_cols, fit=True)
            train = self.scale_numerical_columns(train, num_cols, fit=True)

            # ------------------------ TEST --------------------------#
            test = self.merge_dataset(self.test_df)
            logging.info(f'Columns in merged_test are  :', {test.columns})
            test = self.extract_features(test)
            test = self.handle_missing_values(test, num_cols, fit=False)
            test = self.encode_categorical_columns(test, cat_cols, fit=False)  
            test = self.scale_numerical_columns(test, num_cols, fit=False)

            logging.info('Feature Engineering completed Successfully')
            return train, test

        except Exception as e:
            logging.error(f'Feature Engineering Failed: {str(e)}')
            raise CustomException(e)
