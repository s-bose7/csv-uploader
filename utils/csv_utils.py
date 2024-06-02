# This module should contain functions for reading, parsing, and transforming CSV files 
# before uploading the data to the database.

import pandas as pd
from pandas import DataFrame

from typing import Dict, List
from collections import deque
from db.db_utils import generate_slug
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


def compute_agent_rank(raw_input: DataFrame)->DataFrame:
    if 'agent_rank' not in raw_input.columns:
        raw_input['agent_rank'] = None
    
    # Initialize dictionary to maintain organization email queues
    org_email_dict: Dict[str, List[str]] = {}
    for _, row in raw_input.iterrows():
        slug = generate_slug(row["organization_name"], row["address"])
        if slug not in org_email_dict:
            org_email_dict[slug] = deque(maxlen=3)

        org_email_dict[slug].appendleft(row["contact_email"])    

    for indx, row in raw_input.iterrows():
        slug = generate_slug(row["organization_name"], row["address"])
        raw_input.at[indx, 'agent_rank'] = org_email_dict[slug].index(row["contact_email"]) + 1

    return raw_input


def compute_geom(raw_input: DataFrame)->DataFrame:
    if "geom" not in raw_input.columns:
        raw_input["geom"] = None
    
    return raw_input


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
            # "geom",
            # "irs_ein",
            # "irs_ntee_code",
            # "school_grade",
            # fall_start_date,
            # winter_start_date
        ],
        "club": ["club_name"],
        "contact": [
            "contact_email",
            # "contact_name",
            # "contact_source",
            # "contact_position",
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

    return add_geom_and_agent_rank_columns(raw_input)


def add_geom_and_agent_rank_columns(raw_input: DataFrame)->DataFrame:
    return compute_agent_rank(compute_geom(raw_input))
