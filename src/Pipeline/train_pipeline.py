# src/pipeline/train_pipeline.py

import sys
from src.components.data_ingestion import DataIngestion
from src.components.model_trainer import ModelTrainer
from src.logger import logging
from src.exception import CustomException


class TrainPipeline:
    def __init__(self):
        self.data_ingestion = DataIngestion()
        self.model_trainer = ModelTrainer()

    def run(self):
        try:
            logging.info("========== Training Pipeline Started ==========")

           
            logging.info("Starting data ingestion")
            X_train,X_test, y_train = self.data_ingestion.initiate_data_ingestion()
            logging.info("Data ingestion completed")

            
            logging.info("Starting model training")
            model = self.model_trainer.initiate_model_trainer_linear(X_train, y_train)
            self.model_trainer.print_accuracies()
            logging.info("Model training completed")

            logging.info("========== Training Pipeline Completed ==========")
            
            return model

        except Exception as e:
            logging.error("Error occurred in Training Pipeline")
            raise CustomException(e, sys)
