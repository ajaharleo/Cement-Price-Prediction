from CementStrength.utils.common import *
from CementStrength.constants import *
from pathlib import Path
import numpy as np
import pandas as pd
import dill

@ensure_annotations
def load_data(file_path:Path, schema_file_path:Path)-> pd.DataFrame:
    schema = read_yaml(schema_file_path)
    columns = schema[SCHEMA_COLUMNS_KEY]
    df = pd.read_csv(file_path)
    error_message = ""
    for column in df.columns:
        if column in list(columns.keys()):
            df[column].astype(columns[column])
        else:
            error_message = f"{error_message} \nColumn: [{column}] is not in the schema."
    if len(error_message) > 0:
        raise Exception(error_message)
    return df

@ensure_annotations
def save_numpy_array_data(file_path: Path, array: np.ndarray):
    """
    Save numpy array data to file
    file_path: Path location of file to save
    array: np.array data to save
    """
    dir_path = os.path.dirname(file_path)
    os.makedirs(dir_path, exist_ok=True)
    with open(file_path, 'wb') as file_obj:
        np.save(file_obj, array)

@ensure_annotations
def save_object(file_path:Path,obj):
    """
    file_path: str
    obj: Any sort of object
    """
    dir_path = os.path.dirname(file_path)
    os.makedirs(dir_path, exist_ok=True)
    with open(file_path, "wb") as file_obj:
        dill.dump(obj, file_obj)