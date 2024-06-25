# This module should contain functions for reading, parsing, and transforming CSV files 
# before uploading the data to the database.

import pandas as pd
from pandas import DataFrame
from utils.validators import Validator

from shapely.geometry import Point
from geoalchemy2.shape import from_shape


def read_file(file_path: str)->DataFrame:
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None
    
    return df


def compute_geom(raw_input: DataFrame)->DataFrame:
    if "geom" not in raw_input.columns:
        raw_input["geom"] = None
        
    # Add geom to organizations only if both lat and long exist
    for idx, row in raw_input.iterrows():
        if pd.notnull(row['g_lat']) and pd.notnull(row['g_long']):
            geom = from_shape(
                Point(row['g_long'], row['g_lat']), 
                srid=4326
            )
            raw_input.at[idx, "geom"] = geom
    
    return raw_input


def validate_data(raw_input: DataFrame)->DataFrame:
    missing_columns = Validator.is_missing_columns(raw_input)
    if missing_columns:
        message = (
            f"The following expected columns are missing from the input DataFrame:\n"
            f"{', '.join(missing_columns)}"
        )
        raise ValueError(message)

    raw_input_validated_types = Validator.validate_data_types(raw_input)
    return compute_geom(Validator.drop_duplicates(raw_input_validated_types))


def sanitize_json(data):
    """
    Recursively sanitize JSON data, converting NaN values to None.
    """
    if isinstance(data, dict):
        return {k: sanitize_json(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [sanitize_json(i) for i in data]
    elif pd.isna(data):
        return None
    else:
        return data