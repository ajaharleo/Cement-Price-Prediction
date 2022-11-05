from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionArtifact:
    train_file_path: Path
    test_file_path: Path
    previous_train_file_path: Path
    is_ingested: bool
    message: str

@dataclass(frozen=True)
class DataValidationArtifact:
    schema_file_path: Path
    droppable_columns: list
    report_file_path: Path
    report_page_file_path: Path
    is_validated: bool
    message: str