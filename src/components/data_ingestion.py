import os
import sys
import logging
from src.exception import CustomException
from dataclasses import dataclass
from .data_transformation import DataTransformation
import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


DATA_DIR = PROJECT_ROOT /"notebooks"/ "data"


TRAIN_CSV_PATH = DATA_DIR / "train.csv"
TEST_CSV_PATH = DATA_DIR / "test.csv"
STORE_CSV_PATH = DATA_DIR / "store.csv"

@dataclass
class DataIngestionConfig:
    raw_data_path: str = os.path.join('artifacts', 'raw_data.csv')
    train_data_path: str = os.path.join('artifacts', 'train_data.csv')
    test_data_path: str = os.path.join('artifacts', 'test_data.csv')
class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
        os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)

    def initiate_data_ingestion(self):
        try:
            logging.info('Starting Data Ingestion')

            #currently reading the raw files 
            train_df = pd.read_csv(TRAIN_CSV_PATH)
            test_df = pd.read_csv(TEST_CSV_PATH)
            store_df = pd.read_csv(STORE_CSV_PATH)
            logging.info('Read the raw data as dataframes')
            #saving the raw data files
            train_df.to_csv(self.ingestion_config.raw_data_path, index=False)
            test_df.to_csv(self.ingestion_config.test_data_path, index=False)
            store_df.to_csv(self.ingestion_config.train_data_path, index=False)

            #now performing feature engineering before saving the data
            data_transformation = DataTransformation()
            X_train,X_test,y_train = data_transformation.initiate_data_transformation(train_df, test_df, store_df,'Sales')
            logging.info('Completed Data Transformation')
            #now i can perform the training of the model via the training pipeline

            logging.info('Data Ingestion completed successfully')
            return X_train, X_test, y_train
            

        except Exception as e:
            logging.error(f'Failed Data Ingestion: {str(e)}')
            raise CustomException(f"Error during data ingestion: {str(e)}")
