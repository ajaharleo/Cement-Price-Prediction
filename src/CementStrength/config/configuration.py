from CementStrength.constants import CONFIG_FILE_PATH #, PARAMS_FILE_PATH
from CementStrength.utils import read_yaml, create_directories
from CementStrength.entity.config_entity import DataIngestionConfig
from pathlib import Path
import os

class ConfigurationManager:
    def __init__(
        self, 
        config_filepath = CONFIG_FILE_PATH):
        self.config = read_yaml(config_filepath)
        #self.params = read_yaml(params_filepath)
        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion
        
        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            good_files=config.good_files,
            bad_files=config.bad_files,
            cummilated_csv=config.cummilated_csv,
            archive_bad_files=config.archive_bad_files,
            training_local_db=config.training_local_db,
            prediction_local_db=config.prediction_local_db
        )
        return data_ingestion_config

