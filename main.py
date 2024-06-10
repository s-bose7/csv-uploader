# Orchestrate the data migration process.
import sys
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import db_config
from utils.csv_utils import read_file, validate_data
from db.db_utils import generate_slug, remove_outdated_emails_from_agents
from db.models import Segments, Organizations, Clubs, Contacts, Agents

from shapely.geometry import Point
from geoalchemy2.shape import from_shape


# read raw input
FILE_PATH = "data/csv_files/test_new_agent_rank_logic.csv"
data = read_file(file_path=FILE_PATH)
if data.empty:
    sys.exit(1)

try:
    # transform and validate raw input
    validated_data = validate_data(data)
except ValueError as e:
    logging.error(str(e))
    sys.exit(1)

try:
    ENV = sys.argv[1] if len(sys.argv) > 1 else "-development"
    DATABASE_URL = db_config.get_database_url(environment=ENV)
    # connect to database engine
    engine = create_engine(DATABASE_URL)
except Exception as e:
    logging.error(e)
    sys.exit(1)

# create a new session with the database
Session = sessionmaker(bind=engine)
session = Session()

# insert data
for index, row in validated_data.iterrows():
    
    # Filter segment by name if it exist
    segment = session.query(Segments).filter_by(name=row['organization_category']).first()
    if segment is None:
        # create a segment instance
        segment = Segments(name=row['organization_category'])
        session.add(segment)
        session.commit()
        print(segment.__repr__)

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
            segment_id=segment.id,
            street_address=row['address'],
            latitude=row['g_lat'],
            longitude=row['g_long'],
            city=row['g_city'],
            state=row['g_state'],
            zip=row['g_zip'],
            slug=slug,
            # set custom_fields
            # irs_ein = row["irs_ein"],
            # irs_ntee_code=row["irs_ntee_code"],
            # school_grade=row["school_grade"],
            # fall_start_date=row["fall_start_date"],
            # winter_start_date=row["winter_start_date"],
        )

        # Add geom to organizations only if both lat and long exist
        if row['g_lat'] and row['g_long']:
            organization.geom = from_shape(
                Point(row['g_lat'], row['g_long']), 
                srid=4326
            )

        session.add(organization)
        session.commit()
        print(organization.__repr__)

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

    # Filter contact by email
    contact = session.query(Contacts).filter_by(email=row['contact_email']).first()

    if contact and contact.organization_id != organization.id:
        contact.organization.name = organization.name
        contact.organization.street_address = organization.street_address
        contact.organization.city = organization.city
        contact.organization.state = organization.state
        contact.organization.zip = organization.zip
        contact.organization.slug = generate_slug(organization.name, organization.street_address)
        contact.first_name = row["contact_name"]
        contact.source = row["contact_source"]
        contact.position = row["contact_position"]
        if club is not None:
            contact.club_id = club.id
        session.commit()
        
        # delete this organization
        session.delete(organization)
        session.commit()
        continue
    
    # Filter contact by email and organization.id if it exist
    contact = session.query(Contacts).filter_by(
        email=row['contact_email'],
        organization_id=organization.id
    ).first()

    if contact is None:
        # Create a contact instance
        contact = Contacts (
            email=row['contact_email'],
            organization_id=organization.id,
            # Set other contact fields
            first_name = row["contact_name"],
            source=row["contact_source"],
            position=row["contact_position"]
        )
        # Iff club exist for this contact
        if club is not None: 
            contact.club_id = club.id

        session.add(contact)
        session.commit()
        print(contact.__repr__)

    # Filter agent by contact.id and organization.id if it exist
    agent = session.query(Agents).filter_by(
        contact_id=contact.id,
        organization_id=organization.id
    ).first()

    if agent is None:
        # Create an agent instance
        agent = Agents (
            rank=row['agent_rank'],
            contact_id=contact.id,
            organization_id=organization.id
        )
        # Iff club exist for this agent
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

# prod db appropriate permissions
# custom fields