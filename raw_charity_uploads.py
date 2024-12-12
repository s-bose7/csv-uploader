import csv
import sys
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import db_config
from utils.csv_utils import read_file
from db.models import Charitiy, Organizations

from db.db_utils import generate_slug, add_and_commit


def export_stats(data):
    with open("raw_charity_stats.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(data)

export_stats(["id, charity_name"])
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
    # Process charity
    charity = session.query(Charitiy).filter_by(name=row["name"]).first()
    
    if charity is None:
        # Create an charity instance
        charity = Charitiy (
            name=row["name"],
            address=row["address"],
            city=row["city"],
            state=row["state"],
            zip=row["zip"],
            last_researched_at=row["last_researched_at"],
            irs_ein=row["irs_ein"],
            ntee_code=row["ntee_code"]
        )
        
        add_and_commit(session, charity)
        new_orgs += 1
        export_stats([charity.id, charity.name])
    
    # Relate to organization
    charity_slug = generate_slug(row["name"], row["address"])
    organization = session.query(Organizations).filter_by(slug=charity_slug).first()
    if organization is not None:
        organization.raw_org_id = f"charity_{charity.id}"
        organization.raw_org_type = "charity"

    
export_stats([f"total_charity={total}", f"new_charity={new_orgs}"])
print("\nProcess finished with exit code 0.")