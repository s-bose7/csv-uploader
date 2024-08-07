# Orchestrate the data migration process.
import sys
import logging
import pandas as pd

from config import db_config

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.db_utils import generate_slug
from db.db_utils import add_and_commit
from db.db_utils import remove_agents_with_higher_rank
from db.db_utils import remove_outdated_emails_from_agents

from db.models import Organizations, Clubs, Contacts
from utils.csv_utils import read_file, validate_data, sanitize_json


# Read raw input
FILE_PATH = "data/csv_files/new_file.csv"
data = read_file(file_path=FILE_PATH)
if data.empty:
    sys.exit(1)

try:
    # Transform and validate raw input
    validated_data = validate_data(data)
except ValueError as e:
    logging.error(str(e))
    sys.exit(1)
except Exception as e:
    logging.error(str(e))
    sys.exit(1)

try:
    ENV = sys.argv[1] if len(sys.argv) > 1 else "-development"
    DATABASE_URL = db_config.get_database_url(environment=ENV)
    # Connect to database engine
    engine = create_engine(DATABASE_URL)
except Exception as e:
    logging.error(e)
    sys.exit(1)

# Create a new session with the database
Session = sessionmaker(bind=engine)
session = Session()

# Insert data
for index, row in validated_data.iterrows():

    # Process organization
    # Secondary identifier for organization
    slug = generate_slug(row['organization_name'], row['address'])
    # Filter organization by slug and segment.id if it exist
    organization = session.query(Organizations).filter_by(slug=slug).first()
    
    if organization is None:
        # Create an organization instance
        organization = Organizations (
            name=row['organization_name'],
            slug=slug,
            street_address=row['address'],
            latitude=row['g_lat'],
            longitude=row['g_long'],
            geom=row["geom"],
            city=row['g_city'],
            state=row['g_state'],
            zip=row['g_zip'],
            category=row['organization_category'],
            custom_fields = {},
        )
        if row["created_at"]:
            organization.created_at = row["created_at"]
        # Populate custom_fields
        if row["irs_ein"] and row["irs_ntee_code"]:
            organization.custom_fields["irs_ein"] =  row["irs_ein"]
            organization.custom_fields["irs_ntee_code"] = row["irs_ntee_code"]
        if row["school_grade"]:
            organization.custom_fields["school_grade"] = row["school_grade"]
        if row["charity_source"]:
            organization.custom_fields["charity_source"] = row["charity_source"]
        
        organization.custom_fields = sanitize_json(organization.custom_fields)

        add_and_commit(session, organization)

    # Process clubs
    club: Clubs = None
    if pd.notna(row["club_name"]) and row["club_name"]:
        # Filter club by club name and organization.id if it exist
        club = session.query(Clubs).filter_by(
            name=row['club_name'], 
            organization_id=organization.id
        ).first()
        
        if club is None:
            # Create a club instance
            club = Clubs(name=row['club_name'], organization_id=organization.id)
            add_and_commit(session, club) 
            
    # Process contacts
    # Filter contact by email and organization.id if it exist
    contact: Contacts = None
    if row["contact_email"]:
        contact = session.query(Contacts).filter_by(
            email=row['contact_email'],
            organization_id=organization.id,
        ).first()

        if contact is None:
            # Create a contact instance
            contact = Contacts (
                email=row['contact_email'], 
                organization_id=organization.id,
                custom_fields = {}
            )
            # Populate custom fields
            if row["contact_name"]:
                contact.custom_fields["name"] = row["contact_name"]
            if row["contact_source"]:
                contact.custom_fields["source"] = row["contact_source"]
            if row["contact_position"]:
                contact.custom_fields["position"] = row["contact_position"]

            contact.custom_fields = sanitize_json(contact.custom_fields)

            # If club exist for this contact
            if club is not None: 
                contact.club_id = club.id
            
            add_and_commit(session, contact)
        else:
            # If club exist for this contact and contact already exist in database
            if club is not None: 
                contact.club_id = club.id
            

remove_agents_with_higher_rank(session)
remove_outdated_emails_from_agents(session)

# Close connection
session.close()
engine.dispose()
sys.exit(0)