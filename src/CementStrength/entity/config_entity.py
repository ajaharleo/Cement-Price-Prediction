from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataIngestionConfig:
    dataset_download_url: Path
    raw_data_dir: Path
    ingested_train_dir: Path
    ingested_test_dir: Path



@dataclass(frozen=True)
class DataValidationConfig:
    schema_file_path: Path
    report_file_path: Path
    report_page_file_path: Path


@dataclass(frozen=True)
class DataTransformationConfig:
    transformed_train_dir: Path
    transformed_test_dir: Path
    preprocessed_object_file_path: Path

@dataclass(frozen=True)
class ModelTrainerConfig:
    trained_model_file_path: Path
    base_accuracy: int or float
    model_config_file_path: Path

@dataclass(frozen=True)
class ModelEvaluationConfig:
    model_evaluation_file_path: Path
    time_stamp: any

@dataclass(frozen=True)
class ModelPusherConfig:
    export_dir_path: Path

@dataclass(frozen=True)
class TrainingPipelineConfig:
    artifact_dir: Path