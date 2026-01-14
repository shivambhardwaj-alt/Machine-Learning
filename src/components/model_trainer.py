#now making the model which will be used to train the data
import sys
from src.logger import logging
from src.exception import CustomException
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error ,r2_score
from sklearn.linear_model import LassoLars
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import GridSearchCV
from pathlib import Path
from sklearn.model_selection import train_test_split
PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS_DIR = PROJECT_ROOT / 'artifacts'
MODEL_DIR = ARTIFACTS_DIR / 'train.csv'



class ModelTrainer:
    def __init__(self):
        self.linear_accuracy = None
        self.lasso_accuracy = None
        self.decision_tree_accuracy = None
        self.ridge_accuracy = None


    def initiate_model_trainer_linear(self, X_train, y_train):
        try:
            logging.info("Starting model training process")
            x_train,x_test, y_train, y_test = train_test_split(X_train, y_train, test_size=0.2, random_state=42)


            model = LinearRegression()
            model.fit(x_train, y_train)

            logging.info("Model training completed")

         
            y_pred = model.predict(x_test)

            
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            self.linear_accuracy = r2

            logging.info(f"Model Evaluation - MSE: {mse}, R2 Score: {r2}")

            return model

        except Exception as e:
            logging.error(f"Failed Model Training: {str(e)}")
            raise CustomException(f"Error during model training: {str(e)}")
    def print_accuracies(self):
        logging.info(f"Linear Regression Accuracy: {self.linear_accuracy}")
        logging.info(f"LassoLars Accuracy: {self.lasso_accuracy}")
        logging.info(f"Decision Tree Accuracy: {self.decision_tree_accuracy}")
        logging.info(f"Ridge Regression Accuracy: {self.ridge_accuracy}")
    