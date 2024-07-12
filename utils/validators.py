# This module should contain functions for validating and normalizing the data read from CSV 
# files.

from typing import List, Dict
from pandas import DataFrame

class Validator:

    @staticmethod
    def is_missing_columns(raw_input: DataFrame)->List[str]:
        missing_columns: List[str] = []
        required_columns: Dict[str, List[str]] = {
            "organization": [
                "organization_name",
                "address",
                "g_lat",
                "g_long",
                "g_city",
                "g_state",
                "g_zip",
                "organization_category"
            ],
            "club": ["club_name"],
            "contact": ["contact_email"]
        }
        raw_input_columns = raw_input.columns
        for table, columns in required_columns.items():
            for column in columns:
                if column not in raw_input_columns:
                    missing_columns.append(f"{table}_missing:{column}")

        return missing_columns


    @staticmethod
    def validate_data_types(raw_input: DataFrame)->DataFrame:
        for _, row in raw_input.iterrows():
            if not isinstance(row["segment_name"], str):
                row["segment_name"] = str(row["segment_name"])

            if not isinstance(row["organization_name"], str):
                row["organization_name"] = str(row["organization_name"])
            if not isinstance(row["address"], str):
                row["address"] = str(row["address"])
            if not isinstance(row["g_zip"], str):
                row["g_zip"] = str(row["g_zip"])
            if not isinstance(row["g_lat"], float):
                row["g_lat"] = float(row["g_lat"])
            if not isinstance(row["g_long"], float):
                row["g_long"] = float(row["g_long"])
            
            if not isinstance(row["club_name"], str):
                row["club_name"] = str(row["club_name"])

        return raw_input
    

    @staticmethod
    def drop_duplicates(raw_input: DataFrame)->DataFrame:
        subset = ["organization_name", "contact_email", "club_name"]
        raw_input.drop_duplicates(subset=subset, inplace=True)
        return raw_input    