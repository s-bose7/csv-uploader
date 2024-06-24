# Orchestrate the data migration process.
import sys
import logging

from config import db_config
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.db_utils import generate_slug
from db.db_utils import update_agent_ranks
from db.db_utils import is_most_recent_contact
from db.db_utils import remove_outdated_emails_from_agents

from utils.csv_utils import read_file, validate_data
from db.models import Segments, Organizations, Clubs, Contacts, Agents


# Read raw input
FILE_PATH = "data/csv_files/test.csv"
data = read_file(file_path=FILE_PATH)
if data.empty:
    sys.exit(1)

try:
    # Transform and validate raw input
    validated_data = validate_data(data)
except ValueError as e:
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
    
    # Process segment
    # Filter segment by name if it exist
    segment = session.query(Segments).filter_by(name=row['organization_category']).first()
    if segment is None:
        # create a segment instance
        segment = Segments(name=row['organization_category'])
        session.add(segment)
        session.commit()
        print(segment.__repr__)

    # Process organization
    # Secondary identifier for organization
    slug = generate_slug(row['organization_name'], row['address'])
    
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
            # Set foreign and composite keys
            slug=slug,
            segment_id=segment.id,

            # set custom_fields
            # irs_ein = row["irs_ein"],
            # irs_ntee_code=row["irs_ntee_code"],
            # school_grade=row["school_grade"],
            # fall_start_date=row["fall_start_date"],
            # winter_start_date=row["winter_start_date"],
        )

        session.add(organization)
        session.commit()
        print(organization.__repr__)

    # Process clubs
    club: Clubs = None
    if isinstance(row["club_name"], str) and row["club_name"] != "":
        # Filter club by club name and organization.id if it exist
        club = session.query(Clubs).filter_by(
            name=row['club_name'], 
            organization_id=organization.id
        ).first()
        
        if club is None:
            # Create a club instance
            club = Clubs(name=row['club_name'], organization_id=organization.id)
            session.add(club)
            session.commit()
            print(club.__repr__)    
        
    # Process contacts
    # Filter contact by email and organization.id if it exist
    contact: Contacts = None
    if row["contact_email"] != "":
        contact = session.query(Contacts).filter_by(
            email=row['contact_email'],
            organization_id=organization.id
        ).first()

        if contact is None:
            # Create a contact instance
            contact = Contacts (
                email=row['contact_email'],
                first_name = row["contact_name"],
                source=row["contact_source"],
                position=row["contact_position"],
                # Set foreign key
                organization_id=organization.id,
            )
            # If club exist for this contact
            if club is not None: 
                contact.club_id = club.id

            session.add(contact)
            session.commit()
            print(contact.__repr__)

    # Process agent
    agent: Agents = None
    # Filter agent by contact.id and organization.id if it exist
    if contact is not None:
        agent = session.query(Agents).filter_by(
            contact_id=contact.id,
            organization_id=organization.id
        ).first()
    
    if agent is None and is_most_recent_contact(session, organization, contact):
        update_agent_ranks(session, organization)
        # Create an agent instance
        agent = Agents (
            rank=1, 
            contact_id=contact.id,
            organization_id=organization.id
        )
        # If club exist for this agent
        if club is not None: 
            agent.club_id = club.id

        session.add(agent)
        session.commit()
        print(agent.__repr__)


remove_outdated_emails_from_agents(session)

# Close connection
session.close()
engine.dispose()
sys.exit(0)