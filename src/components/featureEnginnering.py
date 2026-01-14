import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, RobustScaler
from sklearn.impute import SimpleImputer
from src.logger import logging
from src.exception import CustomException
import sys


class FeatureEngineering:
    def __init__(self, train_df: pd.DataFrame, test_df: pd.DataFrame, store_df: pd.DataFrame):
        self.train_df = train_df
        self.test_df = test_df
        self.store_df = store_df

        self.imputer = SimpleImputer(strategy="median")
        self.scaler = RobustScaler()
        self.label_encoders = {}

    def handle_missing_values(self, df, cols, fit=False):
        if fit:
            df[cols] = self.imputer.fit_transform(df[cols])
        else:
            df[cols] = self.imputer.transform(df[cols])
        df[cols] = df[cols].replace([np.inf, -np.inf], np.nan)
        return df

    def merge_dataset(self, df):
        logging.info("Merging store data with main dataset")
        store = self.store_df.drop(
            ['CompetitionOpenSinceMonth', 'CompetitionOpenSinceYear',
             'Promo2SinceWeek', 'Promo2SinceYear', 'PromoInterval'],
            axis=1
        )
        store['CompetitionDistance'].fillna(store['CompetitionDistance'].median(), inplace=True)
        df = df.merge(store, on='Store', how='left')
        logging.info("Merging completed")
        return df

    def extract_features(self, df):
        logging.info("Extracting date features")
        df['Date'] = pd.to_datetime(df['Date'])
        df['Year'] = df['Date'].dt.year
        df['Month'] = df['Date'].dt.month
        df['Day'] = df['Date'].dt.day
        df['WeekOfYear'] = df['Date'].dt.isocalendar().week.astype(int)
        df['DayOfWeek'] = df['Date'].dt.dayofweek
        logging.info("Date features extracted")
        return df

    def encode_categorical_columns(self, df, cols, fit=False):
        logging.info("Encoding categorical columns")
        for col in cols:
            if fit:
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col].astype(str))
                self.label_encoders[col] = le
            else:
                df[col] = self.label_encoders[col].transform(df[col].astype(str))
        logging.info("Categorical columns encoded")
        return df

    def scale_numerical_columns(self, df, cols, fit=False):
        logging.info("Scaling numerical columns")
        if fit:
            df[cols] = self.scaler.fit_transform(df[cols])
        else:
            df[cols] = self.scaler.transform(df[cols])
        logging.info("Numerical columns scaled")
        return df

   
    def perform_feature_engineering(self):
        try:
            logging.info("Feature Engineering started")

            # ---------------- VALIDATION ---------------- #
            if 'Sales' not in self.train_df.columns:
                raise CustomException("Sales column missing in train data", sys)

            # ---------------- MERGE STORE DATA ---------------- #
            train = self.merge_dataset(self.train_df)
            test = self.merge_dataset(self.test_df)

            # ---------------- REMOVE CLOSED DAYS ---------------- #
            # Closed stores always have Sales = 0 → useless noise
            train = train[train['Open'] == 1].copy()

            # ---------------- DATE FEATURES ---------------- #
            train = self.extract_features(train)
            test = self.extract_features(test)

            # ---------------- TARGET TRANSFORMATION ---------------- #
            # Log transform stabilizes variance & improves accuracy
            train['Sales'] = np.log1p(train['Sales'])

            # ---------------- STORE-LEVEL STATISTICS ---------------- #
            # Each store behaves differently → huge accuracy gain
            store_stats = train.groupby('Store')['Sales'].agg(
                Store_Sales_Mean='mean',
                Store_Sales_Median='median',
                Store_Sales_STD='std'
            ).reset_index()

            train = train.merge(store_stats, on='Store', how='left')
            test = test.merge(store_stats, on='Store', how='left')

            # ---------------- PROMO INTERACTIONS ---------------- #
            train['PromoHoliday'] = ((train['Promo'] == 1) & (train['SchoolHoliday'] == 1)).astype(int)
            test['PromoHoliday'] = ((test['Promo'] == 1) & (test['SchoolHoliday'] == 1)).astype(int)

            # ---------------- COLUMN GROUPS ---------------- #
            train_num_cols = [
                'CompetitionDistance',
                'Store_Sales_Mean',
                'Store_Sales_Median',
                'Store_Sales_STD'
            ]

            test_num_cols = train_num_cols.copy()

            cat_cols = ['StoreType', 'Assortment', 'StateHoliday']

            # ---------------- MISSING VALUES ---------------- #
            train = self.handle_missing_values(train, train_num_cols, fit=True)
            test = self.handle_missing_values(test, test_num_cols, fit=False)

            # ---------------- ENCODING ---------------- #
            train = self.encode_categorical_columns(train, cat_cols, fit=True)
            test = self.encode_categorical_columns(test, cat_cols, fit=False)

            # ---------------- SCALING ---------------- #
            train = self.scale_numerical_columns(train, train_num_cols, fit=True)
            test = self.scale_numerical_columns(test, test_num_cols, fit=False)

            # ---------------- FINAL FEATURE SELECTION ---------------- #
            drop_cols = ['Sales', 'Customers', 'Date']
            X_train = train.drop(columns=drop_cols)
            y_train = train['Sales']

            X_test = test.drop(columns=['Date'])

            logging.info("Feature Engineering completed successfully")

            return X_train, y_train, X_test

        except Exception as e:
            logging.error(f"Feature Engineering failed: {e}")
            raise CustomException(e, sys)
