from CementStrength.constants import * 
from CementStrength.utils import *
from CementStrength.entity import DataIngestionConfig,DataValidationConfig
from pathlib import Path
import os
from CementStrength import logger

class Configuration:
    def __init__(self,
                config_file_path:str = CONFIG_FILE_PATH,
                current_time_stamp:str = get_current_time_stamp()
                ) -> None:
        self.config_info = read_yaml(config_file_path)
        self.artifact_dir = os.path.join(ROOT_DIR,
                            self.config_info.training_pipeline_config.pipeline_name+'_'+
                            self.config_info.training_pipeline_config.artifact_dir)
        self.time_stamp = current_time_stamp
        

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        artifact_dir = self.artifact_dir
        data_ingestion_artifact_dir = os.path.join(artifact_dir,
                                        DATA_INGESTION_ARTIFACT_DIR,
                                        self.time_stamp)

        data_ingestion_info = self.config_info[DATA_INGESTION_CONFIG_KEY]
        dataset_download_url = data_ingestion_info[DATA_INGESTION_DOWNLOAD_URL_KEY]
        raw_data_dir = os.path.join(data_ingestion_artifact_dir,
                        data_ingestion_info[DATA_INGESTION_RAW_DATA_DIR_KEY])

        ingested_dir = os.path.join(data_ingestion_artifact_dir,
                        data_ingestion_info[DATA_INGESTION_INGESTED_DIR_NAME_KEY])
        ingested_train_dir = os.path.join(ingested_dir,
                            data_ingestion_info[DATA_INGESTION_TRAIN_DIR_KEY])
        ingested_test_dir = os.path.join(ingested_dir,
                            data_ingestion_info[DATA_INGESTION_TEST_DIR_KEY])

        data_ingestion_config = DataIngestionConfig(
                                dataset_download_url=dataset_download_url, 
                                raw_data_dir=raw_data_dir, 
                                ingested_train_dir=ingested_train_dir, 
                                ingested_test_dir=ingested_test_dir
        )
        logger.info(f'DataIngestionConfig: {data_ingestion_config}')
        return data_ingestion_config


    def get_data_validation_config(self) -> DataValidationConfig:
        artifact_dir = self.artifact_dir
        data_validation_info = self.config_info[DATA_VALIDATION_CONFIG_KEY]
        data_validation_artifact_dir = os.path.join(artifact_dir,
                                                    DATA_VALIDATION_ARTIFACT_DIR,
                                                    self.time_stamp)
        report_file_path = os.path.join(data_validation_artifact_dir,
                                        data_validation_info[DATA_VALIDATION_REPORT_FILE_NAME_KEY])
        report_page_file_path = os.path.join(data_validation_artifact_dir,
                                            data_validation_info[DATA_VALIDATION_REPORT_PAGE_FILE_NAME_KEY])
        schema_file_path =Path( os.path.join(ROOT_DIR,
                                        data_validation_info[DATA_VALIDATION_SCHEMA_DIR_KEY],
                                        data_validation_info[DATA_VALIDATION_SCHEMA_FILE_NAME_KEY]))
        data_validation_config = DataValidationConfig(schema_file_path=schema_file_path,
                                                        report_file_path=report_file_path,
                                                        report_page_file_path=report_page_file_path)
        logger.info(f"DataValidationConfig: {data_validation_config}")
        return data_validation_config
