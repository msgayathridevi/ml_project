# read dataset from specific source and split the dataset into train test
# convert the eda and training into modular programming using data ingestion, transformation and model trainder.py files
 
import os
import sys  # to use custom exception

# from pathlib import Path
# sys.path.append(str(Path(__file__).parent.parent.parent))

from src.exception import CustomException
from src.logger import logging

import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass # create class variable

from src.components.data_transformation import DataTransformation
# from src.components.data_transformation import DataTransformationConfig

from src.components.model_trainer import ModelTrainer
# from src.components.model_trainer import ModelTrainerConfig

# requiring some input configs for data ingestion component can be written in a separate class
@dataclass
class DataIngestionConfig:
    # in artifacts all the op folders will be saved
    train_data_path : str = os.path.join('artifacts', "train.csv")
    test_data_path : str = os.path.join('artifacts', "test.csv")
    raw_data_path : str = os.path.join('artifacts', "data.csv")

class DataIngestion:
    def __init__(self):
        # all the 3 artifacts will be saved in ingestion_config
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Entered teh data ingestion method or component")
        try:
            # can read from different sources
            # for now I fetched locally
            df = pd.read_csv('notebook\data\student_performance.csv') # can read from different sources
            logging.info("Read teh dataset as dataframe")

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok = True)

            df.to_csv(self.ingestion_config.train_data_path, index = False, header = True)
            logging.info("Train test split initiated")

            train_set, test_set = train_test_split(df, test_size = 0.2, random_state = 42)

            train_set.to_csv(self.ingestion_config.train_data_path, index = False, header = True)
            test_set.to_csv(self.ingestion_config.test_data_path, index = False, header = True)

            logging.info("Ingestion fo the data is completed")
            
            # return the train and test data path
            # for data transformation
            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        
        except Exception as e:
            # pass
            raise CustomException(e, sys)

if __name__=="__main__":
    obj = DataIngestion()
    # obj.initiate_data_ingestion()
    train_data, test_data = obj.initiate_data_ingestion()

    data_transformation = DataTransformation()
    # data_transformation.initiate_data_transformation(train_data, test_data)
    train_arr, test_arr, _ = data_transformation.initiate_data_transformation(train_data, test_data)

    model_trainer = ModelTrainer()
    # model_trainer.initiate_model_trainer(train_arr, test_arr)
    print(model_trainer.initiate_model_trainer(train_arr, test_arr))

# next step data transformation