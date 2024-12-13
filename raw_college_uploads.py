import csv
import sys
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import db_config
from utils.csv_utils import read_file
from db.models import College, Organizations

from db.db_utils import generate_slug, add_and_commit


def export_stats(data):
    with open("raw_colleges_stats.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(data)

export_stats(["id", "slug"])
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
    college = session.query(College).filter_by(url=row["url"]).first()
    
    if college is None:
        # Create an college instance
        college = College (
            name=row["name"],
            address=row["address"],
            city=row["city"],
            state=row["state"],
            zip=row["zip"],
            last_researched_at=row["last_researched_at"],
            url=row["url"],
            campuslabs=row["campuslabs"],
            has_clubs_to_collect=row["has_clubs_to_collect"]
        )

        add_and_commit(session, college)
        new_orgs += 1
        export_stats([college.id, college.url])
    
    # Relate to organization
    college_slug = generate_slug(row["name"], row["address"])
    organization = session.query(Organizations).filter_by(slug=college_slug).first()
    if organization is not None:
        organization.raw_org_id = f"college_{college.id}"
        organization.raw_org_type = "college"
        college.last_researched_at = organization.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        add_and_commit(session, college)

    
export_stats([f"total_colleges={total}", f"new_colleges={new_orgs}"])
print("\nProcess finished with exit code 0.")