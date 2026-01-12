import os 
import joblib
from src.logger import logging
from src.exception import CustomException
from src.components.featureEnginnering import FeatureEngineering

class DataTransformation:
    def __init__(self):
        self.artifact_dir = "artifacts"
        os.makedirs(self.artifact_dir, exist_ok=True)

    def initiate_data_transformation(self, train_df, test_df, store_df, target_col):
        try:
            logging.info('Starting Data Transformation')
            print(train_df.head())

           
            fe = FeatureEngineering(train_df, test_df, store_df)
            
            
            train_processed, test_processed = fe.perform_feature_engineering()

           
            X_train = train_processed.drop(columns=[target_col])
            y_train = train_processed[target_col]

            X_test = test_processed.drop(columns=[target_col])
            y_test = test_processed[target_col]

            logging.info('Trying to convert the dataframe into the csv files')

            # Save the processed datasets into CSV files
            train_processed.to_csv(os.path.join(self.artifact_dir, 'train_processed.csv'), index=False)
            test_processed.to_csv(os.path.join(self.artifact_dir, 'test_processed.csv'), index=False)

            logging.info('Conversion of the files successful')

            # Return the transformed data
            return X_train, X_test, y_train, y_test
        
        except Exception as e: 
           
            logging.error(f'Failed Data Transformation: {str(e)}')
            raise CustomException(f"Error during data transformation: {str(e)}")

