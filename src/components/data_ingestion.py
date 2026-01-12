import os
import sys
from src.logger import logging
from src.exception import CustomException
import pandas as pd
from sklearn.model_selection import train_test_split
from Pipeline.featureEnginnering import FeatureEngineering
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    train_data_path: str =  os.path.join('artifacts','train.csv')
    test_data_path : str  =  os.path.join('artifacts','test.csv')
    raw_data_path : str = os.path.join("artifacts",'data.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
    def intiate_data_ingestion(self):
        logging.info("Entered into the ingestion part")
        try:

            logging.info("Reading the datasets")
            train_df = pd.read_csv('./notebooks/data/train.csv')
            test_df = pd.read_csv('./notebooks/data/test.csv')
            store_df = pd.read_csv('./notebooks/data/store.csv')
            logging.info("DataSets are read successfully")
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)
            train_df.to_csv(self.ingestion_config.raw_data_path)
            logging.info("Raw data saved at: %s", self.ingestion_config.raw_data_path)
            logging.info("FeatureEngineering is performing")
            FeatureEngineering = FeatureEngineering(train_df,test_df,store_df)
            train_featured = FeatureEngineering.perform_feature_engineering()
            test_featured = FeatureEngineering.perform_feature_engineering()



        except:
            pass
