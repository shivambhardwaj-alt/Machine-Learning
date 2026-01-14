import sys
from src.logger import logging
from src.exception import CustomException
from src.components.data_ingestion import DataIngestion
from src.Pipeline.train_pipeline import TrainPipeline

def main():
    try:
        logging.info("Starting data ingestion process")
        

        logging.info("Starting training pipeline")
        train_pipeline = TrainPipeline()
        model = train_pipeline.run()

    

    except Exception as e:
        raise CustomException(e, sys)


if __name__ == "__main__":
    main()
