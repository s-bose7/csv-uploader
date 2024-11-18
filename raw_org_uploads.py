import csv
import sys
import logging

from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import db_config
from utils.csv_utils import read_file
from db.models import Organizations

from db.db_utils import generate_slug, add_and_commit


def export_stats(data):
    with open("raw_orgs_stats.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(data)

export_stats(["id, slug"])
FILE_PATH = "data/csv_files/raw_orgs - Sheet1.csv"
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
    # Process organization
    # Secondary identifier for organization
    slug = generate_slug(row['organization_name'], row['organization_address'])
    # Filter organization by slug and segment.id if it exist
    organization = session.query(Organizations).filter_by(slug=slug).first()
    
    if organization is None:
        # Create an organization instance
        organization = Organizations (
            name=row['organization_name'],
            slug=slug,
            street_address=row['organization_address'],
            city=row['organization_city'],
            state=row['organization_state'],
            zip=row['organization_zip'],
            custom_fields = {},
        )
        organization.created_at = datetime.now()
        if row["irs_ein"] is not None and row["irs_ntee_code"] is not None:
            organization.custom_fields["irs_ein"] =  row["irs_ein"]
            organization.custom_fields["irs_ntee_code"] = row["irs_ntee_code"]

        add_and_commit(session, organization)
        new_orgs += 1
        export_stats([organization.id, organization.slug])
    
export_stats([f"total_orgs={total}", f"new_orgs={new_orgs}"])
print("\nProcess finished with exit code 0.")