import os,sys
import pandas as pd
from CementStrength.constants import *
from CementStrength.entity import DataIngestionConfig, DataValidationConfig,DataIngestionArtifact,DataValidationArtifact
from CementStrength.utils import *
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab
from CementStrength import logger
import numpy as np
import json

class DataValidation:
    def __init__(self,
                data_validation_config: DataValidationConfig,
                data_ingestion_artifact: DataIngestionArtifact) -> None:
        logger.info(f"{'='*20} Data Validation Log Started {'='*20}")
        self.data_validation_config = data_validation_config
        self.data_ingestion_artifact = data_ingestion_artifact
        self.train_file_path = self.data_ingestion_artifact.train_file_path
        self.test_file_path = self.data_ingestion_artifact.test_file_path
        self.train_df = pd.read_csv(self.train_file_path)
        self.test_df = pd.read_csv(self.test_file_path)
        self.schema = read_yaml(self.data_validation_config.schema_file_path)
        self.previous_train_file_path = self.data_ingestion_artifact.previous_train_file_path
        self.previous_train_df = pd.read_csv(self.previous_train_file_path)

    def do_train_test_files_exist(self)-> True:
        try:
            logger.info("Checking if test and train file exists.")
            does_train_file_exist = False
            does_test_file_exist = True
            does_train_file_exist = os.path.exists(self.train_file_path)
            does_test_file_exist = os.path.exists(self.test_file_path)
            if not does_train_file_exist:
                raise Exception(f"Train file: [{self.train_file_path}] does not exists.")
            if not does_test_file_exist:
                raise Exception(f"Test file: [{self.test_file_path}] does not exists.")
            if does_test_file_exist and does_train_file_exist:
                logger.info(f"Both train file: [{self.train_file_path}] and test file: [{self.test_file_path} exist.")
                return True
        except Exception as e:
            logger.exception(e)

    def validate_dataset_schema(self)-> True:
        try:
            schema_columns = self.schema[SCHEMA_COLUMNS_KEY]
            schema_domain_value = self.schema[SCHEMA_DOMAIN_VALUE_KEY]
            schema_numerical_columns = self.schema[SCHEMA_NUMERICAL_COLUMNS_KEY]
            schema_categorical_columns = self.schema[SCHEMA_CATEGORICAL_COLUMNS_KEY]
            logger.info("Checking no. of columns in train and test dataset")
            check_no_of_columns = len(schema_columns) == len(self.train_df.columns) and len(schema_columns) == len(self.test_df.columns)
            if not check_no_of_columns:
                raise Exception("Train and/or test dataset does not have columns given in schema.")
            else:
                logger.info('No. of columns are same in train and test dataset and in schema file.')
                logger.info("Checking columns names")
                for column in schema_columns.keys():
                    if column not in self.train_df.columns:
                        raise Exception(f"Train dataset does not have column '{column}' required in schema file")
                    if column not in self.test_df.columns:
                        raise Exception(f"Test dataset does not have column '{column}' required in schema file")
                else:
                    logger.info(f"Train and test dataset have column required in schema file")
            logger.info("Checking the datatypes of all columns")
            for column in schema_columns.keys():
                if self.train_df[column].dtype == schema_columns[column]:
                    logger.info(f"Column '{column}' has correct datatype.")
                else:
                    raise Exception(f"Column '{column}' does not have correct datatype.")
            logger.info("Checking the domain values of categorical columns")
            for column, cats in schema_domain_value.items():
                logger.info(f"Checking domain values of column '{column}'")
                for cat in self.train_df[column].unique():
                    if cat not in schema_domain_value[column]:
                        raise Exception(f"category '{cat}' is an unwanted value in column '{column}' of test dataset")
                for cat in self.test_df[column].unique():
                    if cat not in schema_domain_value[column]:
                        raise Exception(f"category '{cat}' is an unwanted value in column '{column}' of test dataset")
                else:
                    logger.info(f"column '{column}' has all the required categories and no extra category")
            logger.info("Data Validation Successful!")
            return True
        except Exception as e:
            logger.exception(e)

    def check_for_correlation(self):
        try:
            logger.info("Checking correlation between features")
            df  = self.train_df.copy(deep=True)
            target_column = self.schema[SCHEMA_TARGET_COLUMN_KEY][0]
            droppable_columns = []
            corr_matrix = df.corr(method='spearman')
            for column in df.columns:
                if np.abs(corr_matrix.loc[column,target_column]) < 0.1:
                    logger.info(f"Column [{column}] has very less correlation with the target feature.")
                    droppable_columns.append(column)
                    df.drop(column, axis=1, inplace=True)
            for i in df.drop(target_column,axis=1).columns:
                for j in df.drop(target_column,axis=1).columns:
                    if not i==j:
                        if corr_matrix.loc[i,j] > 0.7:
                            logger.info(f"Column [{i}[] and [{j}] has very high dependence on each other.")
                            df.drop(i, axis=1, inplace=True)
                            droppable_columns.append(column)
            logger.info(f"Droppable columns: {droppable_columns}")
            return droppable_columns
        except Exception as e:
            logger.exception(e)

    def get_and_save_data_drift_report(self):
        try:
            profile = Profile(sections = [DataDriftProfileSection()])
            profile.calculate(self.train_df, self.previous_train_df)
            report = json.loads(profile.json())
            report_file_path = self.data_validation_config.report_file_path
            os.makedirs(os.path.dirname(report_file_path), exist_ok=True)
            with open(self.data_validation_config.report_file_path, "w") as report_file:
                json.dump(report, report_file, indent=4)
                return report
        except Exception as e:
            logger.exception(e)

    def save_data_drift_report_page(self):
        try:
            dashboard = Dashboard(tabs= [DataDriftTab()])
            dashboard.calculate(self.train_df, self.previous_train_df)
            dashboard.save(self.data_validation_config.report_page_file_path)
        except Exception as e:
            logger.exception(e)

    def does_data_drift_occur(self)-> bool:
        try:
            report = self.get_and_save_data_drift_report()
            self.save_data_drift_report_page()
            return True
        except Exception as e:
            logger.exception(e)

    def initiate_data_validation(self)-> DataValidationArtifact:
        try:
            self.do_train_test_files_exist()
            validation_status =self.validate_dataset_schema()
            self.does_data_drift_occur()
            droppable_columns = self.check_for_correlation()
            data_validation_artifact = DataValidationArtifact(schema_file_path=self.data_validation_config.schema_file_path,
                                                            droppable_columns= droppable_columns,
                                                            report_file_path=self.data_validation_config.report_page_file_path,
                                                            report_page_file_path=self.data_validation_config.report_page_file_path,
                                                            is_validated=validation_status,
                                                            message="Data Validation performed sucessfully.")
            logger.info(f"Data Validation Artifact : {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            logger.exception(e)

    def __del__(self):
        logger.info(f"{'='*20}Data Validation log ended{'='*20} \n\n")