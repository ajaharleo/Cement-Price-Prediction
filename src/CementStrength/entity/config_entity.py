from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    good_files: Path
    bad_files: Path
    cummilated_csv: Path
    archive_bad_files: Path
    training_local_db: Path
    prediction_local_db: Path