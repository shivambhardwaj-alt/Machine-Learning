import os
import sys
from src.logger import logging
from src.exception import CustomException
import pandas as pd
from dataclasses import dataclass
from src.components.data_transformation import DataTransformation  # Correct import
from src.components.featureEnginnering import FeatureEngineering

@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', 'train.csv')
    test_data_path: str = os.path.join('artifacts', 'test.csv')
    raw_data_path: str = os.path.join('artifacts', 'data.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None

    def initiate_data_ingestion(self):
        logging.info("Entered into the ingestion part")
        try:
            logging.info("Reading the datasets")
            
           
            train_df = pd.read_csv(os.path.join('notebooks', 'data', 'train.csv'))
            test_df = pd.read_csv(os.path.join('notebooks', 'data', 'test.csv'))
            store_df = pd.read_csv(os.path.join('notebooks', 'data', 'store.csv'))
            
            logging.info("Datasets are read successfully")

        
            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)
            logging.info(f"Saving raw data at: {self.ingestion_config.raw_data_path}")
            train_df.to_csv(self.ingestion_config.raw_data_path)  # Save the raw data
            logging.info(f"Raw data saved at: {self.ingestion_config.raw_data_path}")

            data_transformation = DataTransformation()
            X_train, X_test, y_train, y_test = data_transformation.initiate_data_transformation(train_df, test_df, store_df, target_col='Sales')

            logging.info("Ingestion completed!")

         
            self.X_train = X_train
            self.X_test = X_test
            self.y_train = y_train
            self.y_test = y_test

            return X_train, X_test, y_train, y_test

        except Exception as e:
            logging.error(f"Failed to Data Ingestion: {str(e)}")
            raise CustomException(e)

if __name__ == "__main__":
    obj = DataIngestion()
    obj.initiate_data_ingestion()
