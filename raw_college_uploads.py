import csv
import sys
import logging

from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import db_config
from utils.csv_utils import read_file
from db.models import College

from db.db_utils import generate_slug, add_and_commit


def export_stats(data):
    with open("raw_colleges_stats.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(data)

export_stats(["id, slug"])
FILE_PATH = "data/csv_files/" # pass file path here
data = read_file(file_path=FILE_PATH)

try:
    ENV = sys.argv[1] if len(sys.argv) > 1 else "-development"
    DATABASE_URL = db_config.get_database_url(environment=ENV)
    # Connect to database engine
    engine = create_engine(DATABASE_URL)
except Exception as e:
    logging.error(e)
    sys.exit(1)


Session = sessionmaker(bind=engine)
session = Session()

total = 0
new_orgs = 0

for index, row in data.iterrows():
    
    total += 1
    # Process colleges
    college = session.query(College).filter_by(college_url=row["college_url"]).first()
    
    if college is None:
        # Create an college instance
        college = College (
            nces_data=row["nces_data"],
            last_researched_at=row["last_researched_at"],
            college_url=row["college_url"],
            campuslabs=row["campuslabs"],
            has_clubs_to_collect=row["has_clubs_to_collect"]
        )
        
        add_and_commit(session, college)
        new_orgs += 1
        export_stats([college.id, college.college_url])
    
export_stats([f"total_colleges={total}", f"new_colleges={new_orgs}"])
print("\nProcess finished with exit code 0.")