# This module should contain functions for reading, parsing, and transforming CSV files 
# before uploading the data to the database.

import pandas as pd
from pandas import DataFrame

from validators import Validator


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
    
    expected_columns = {
        "segment": ["organization_category"],
        "organization": [
            "organization_name",
            "address",
            "g_lat",
            "g_long",
            "g_city",
            "g_state",
            "g_zip",
            "irs_ein",
            "irs_ntee_code",
            "school_grade",
            # geom,
            # fall_start_date,
            # winter_start_date
        ],
        "club": ["club_name"],
        "contact": [
            "contact_name",
            "contact_email",
            "contact_source",
            "contact_position",
        ],
    }

    missing_columns = []
    for table, columns in expected_columns.items():
        for col in columns:
            if col not in raw_input.columns:
                missing_columns.append(f"{table}.{col}")

    if missing_columns:
        message = (
            f"The following expected columns are missing from the input DataFrame:\n"
            f"{', '.join(missing_columns)}"
        )
        raise ValueError(message)

    return raw_input