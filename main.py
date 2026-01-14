import sys
from src.logger import logging
from src.exception import CustomException
from src.components.data_ingestion import DataIngestion


def main():
    try:
        logging.info("Starting data ingestion process")
        DataIngestion().initiate_data_ingestion()

    except CustomException:
        # Already logged inside CustomException
        raise

    except Exception as e:
        raise CustomException(e, sys)


if __name__ == "__main__":
    main()
