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