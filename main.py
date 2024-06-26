# Orchestrate the data migration process.
import os
import sys
import logging
import pandas as pd

from config import db_config

from datetime import datetime
from typing import List, Dict, Tuple

from db.uploader import clubs
from db.uploader import agents
from db.uploader import segments
from db.uploader import contacts
from db.uploader import organizations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.db_utils import generate_slug
from db.db_utils import update_agent_ranks
from db.db_utils import is_most_recent_contact
from db.db_utils import remove_outdated_emails_from_agents

from utils.csv_utils import read_file
from utils.csv_utils import sanitize_json
from utils.csv_utils import validate_data

from db.models import Segments, Organizations, Clubs, Contacts, Agents


# Read raw input
FILE_PATH = "data/csv_files/group_contacts.csv"
print(f"[{datetime.now()}] Reading files...")
data = read_file(file_path=FILE_PATH)
print(f"[{datetime.now()}] DONE")
if data.empty:
    sys.exit(1)

try:
    # Transform and validate raw input
    print(f"[{datetime.now()}] Validating data...")
    validated_data = validate_data(data)
    print(f"[{datetime.now()}] DONE")
except ValueError as e:
    logging.error(str(e))
    sys.exit(1)
except Exception as e:
    logging.error(str(e))
    sys.exit(1)

try:
    print(f"[{datetime.now()}] Connecting to the database...")
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
print(f"[{datetime.now()}] DONE")

print(f"[{datetime.now()}] Starting the uploading process...")
# Process segment
segment_cache: Dict[str, Segments] = {}
segments_to_add: List[Segments] = []

for index, row in validated_data.iterrows():
    segment_name = row["segment_name"]
    if segment_name not in segment_cache:     
        # Filter segment by name if it exist
        segment = session.query(Segments).filter_by(name=segment_name).first()
        if segment is None:
            # create a segment instance
            segment = Segments(name=segment_name)
            segments_to_add.append(segment)

        segment_cache[segment_name] = segment 

session.bulk_save_objects(segments_to_add)
session.commit()

for segment in segments_to_add:
    segment_with_id = session.query(Segments).filter_by(name=segment.name).first()
    segment_cache[segment.name] = segment_with_id

print(f"[{datetime.now()}] Successfully uploaded {len(segments_to_add)} segments.")

# Process organization
organization_cache: Dict[Tuple[str, int], Organizations] = {}
organizations_to_add: List[Organizations] = []

for _, row in validated_data.iterrows():
    segment = segment_cache.get(row["segment_name"])
    # Secondary identifier for organization
    slug = generate_slug(row['organization_name'], row['address'])
    organization_key = (slug, segment.id)
    if organization_key not in organization_cache:
        # Filter organization by slug and segment.id if it exist
        organization = session.query(Organizations).filter_by(
            slug=slug, 
            segment_id=segment.id
        ).first()
    
        if organization is None:
            # Create an organization instance
            organization = Organizations (
                name=row['organization_name'],
                street_address=row['address'],
                latitude=row['g_lat'],
                longitude=row['g_long'],
                geom=row["geom"],
                city=row['g_city'],
                state=row['g_state'],
                zip=row['g_zip'],
                category=row['organization_category'],
                custom_fields = {},
                # Set foreign and composite keys
                slug=slug,
                segment_id=segment.id,
            )
            if row["created_at"]:
                organization.created_at = row["created_at"]
            # Populate custom_fields
            if row["irs_ein"] and row["irs_ntee_code"]:
                organization.custom_fields["irs_ein"] =  row["irs_ein"]
                organization.custom_fields["irs_ntee_code"] = row["irs_ntee_code"]
            if row["school_grade"]:
                organization.custom_fields["school_grade"] = row["school_grade"]
            
            organization.custom_fields = sanitize_json(organization.custom_fields)
            organizations_to_add.append(organization)
        
        organization_cache[organization_key] = organization

session.bulk_save_objects(organizations_to_add)
session.commit()

for orgs in organizations_to_add:
    orgs_with_id = session.query(Organizations).filter_by(
        slug = orgs.slug,
        segment_id = orgs.segment_id
    ).first()
    organization_cache[(orgs.slug, orgs.segment_id)] = orgs_with_id

print(f"[{datetime.now()}] Successfully uploaded {len(organizations_to_add)} organizations.")


# Process clubs
club_cache: Dict[Tuple[str, int], Clubs] = {}
clubs_to_add: List[Clubs] = []

for _, row in validated_data.iterrows():
    segment = segment_cache.get(row["segment_name"])
    slug = generate_slug(row['organization_name'], row['address'])
    organization = organization_cache.get((slug, segment.id))

    if pd.notna(row["club_name"]) and row["club_name"]:
        club_key = (row["club_name"], organization.id)
        if club_key not in club_cache:
            # Filter club by club name and organization.id if it exist
            club = session.query(Clubs).filter_by(
                name=row['club_name'], 
                organization_id=organization.id
            ).first()
            
            if club is None:
                # Create a club instance
                club = Clubs(name=row['club_name'], organization_id=organization.id)
                clubs_to_add.append(club)

            club_cache[club_key] = club    

session.bulk_save_objects(clubs_to_add)
session.commit()

for club in clubs_to_add:
    club_with_id = session.query(Clubs).filter_by(
        name=club.name, 
        organization_id=club.organization_id
    ).first()
    club_cache[(club.name, club.organization_id)] = club_with_id
 
print(f"[{datetime.now()}] Successfully uploaded {len(clubs_to_add)} clubs.")

# Process contacts
contact_cache: Dict[Tuple[str, int], Contacts] = {}
contacts_to_add: List[Contacts] = []

for _, row in validated_data.iterrows():
    segment = segment_cache.get(row["segment_name"])
    slug = generate_slug(row['organization_name'], row['address'])
    organization = organization_cache.get((slug, segment.id))
    club = club_cache.get((row["club_name"], organization.id))

    if row["contact_email"]:
        contact_key = (row["contact_email"], organization.id)
        if contact_key not in contact_cache:
            # Filter contact by email and organization.id if it exist
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

                contacts_to_add.append(contact)

            contact_cache[contact_key] = contact

session.bulk_save_objects(contacts_to_add)
session.commit()

for contact in contacts_to_add:
    contact_with_id = session.query(Contacts).filter_by(
        email=contact.email,
        organization_id=contact.organization_id
    ).first()
    contact_cache[(contact.email, contact.organization_id)] = contact_with_id

print(f"[{datetime.now()}] Successfully uploaded {len(contacts_to_add)} contacts.")

# Process agent
agents_to_add: List[Agents] = []

for _, row in validated_data.iterrows():
    segment = segment_cache.get(row["segment_name"])
    slug = generate_slug(row['organization_name'], row['address'])
    organization = organization_cache.get((slug, segment.id))
    club = club_cache.get((row["club_name"], organization.id))
    contact = contact_cache.get((row["contact_email"], organization.id))

    # Filter agent by contact.id and organization.id if it exist
    if contact is not None:
        agent = session.query(Agents).filter_by(
            contact_id=contact.id, organization_id=organization.id
        ).first()

    if agent is None and is_most_recent_contact(session, organization, contact):
        update_agent_ranks(session, organization)
        # Create an agent instance
        agent = Agents (
            rank = 1, 
            contact_id=contact.id,
            organization_id=organization.id
        )
        # If club exist for this agent
        if club is not None: 
            agent.club_id = club.id
    
        agents_to_add.append(agent)

session.bulk_save_objects(agents_to_add)
session.commit()
print(f"[{datetime.now()}] Successfully uploaded {len(agents_to_add)} agents.")

remove_outdated_emails_from_agents(session)

# Close connection
session.close()
engine.dispose()
print(f"[{datetime.now()}] DONE")
sys.exit(0)