# This module should contain functions for reading, parsing, and transforming CSV files 
# before uploading the data to the database.

import pandas as pd
from pandas import DataFrame

from utils.validators import Validator


def read_file(file_path: str, file_type="csv")->DataFrame:
    try:
        if file_type == "csv":
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None
    
    return df


def validate_data(raw_input: DataFrame)->DataFrame:
    return raw_input
    