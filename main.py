# Orchestrate the data migration process.
import os
import sys
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.models import (
    Segments,
    Organizations,
    Clubs,
    Contacts,
    Agents
)

from config import db_config
from utils.csv_utils import read_file, validate_data

# read raw input
FILE_PATH = "data/csv_files/test.csv"
data = read_file(file_path=FILE_PATH)
if data == None: sys.exit(1)

try:
    # transform and validate raw input
    validated_data = validate_data(data)
except ValueError as e:
    logging.error(str(e))
    sys.exit(1)

try:
    ENV = sys.argv[1] if len(sys.argv) > 1 else "development"
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
    
    # filter segment by name if it exist
    segment = session.query(Segments).filter_by(name=row['organization_category']).first()
    if segment is None:
        # create a segment instance
        segment = Segments(name=row['organization_category'])
        session.add(segment)
        session.commit()
        print(segment.__repr__)

    # secondary identifier for organization
    slug = str(row['organization_name'] + str(row['address'])).replace(" ", "").lower()
    
    # filter organization by slug and segment.id if it exist
    organization = session.query(Organizations).filter_by(
        slug=slug, 
        segment_id=segment.id
    ).first()
    
    if organization is None:
        # create an organization instance
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
            # set other org fields
            irs_ein = row["irs_ein"],
            irs_ntee_code=row["irs_ntee_code"],
            school_grade=row["school_grade"],
            # deprecated columns
            # geom=row["geom"],
            # fall_start_date=row["fall_start_date"],
            # winter_start_date=row["winter_start_date"],
        )
        session.add(organization)
        session.commit()
        print(organization.__repr__)

    club: Clubs = None
    if isinstance(row["club_name"], str) and row["club_name"] != "":
        # filter club by club name and organization.id if it exist
        club = session.query(Clubs).filter_by(
            name=row['club_name'], 
            organization_id=organization.id
        ).first()
        
        if club is None:
            # create a club instance
            club = Clubs(name=row['club_name'], organization_id=organization.id)
            session.add(club)
            session.commit()
            print(club.__repr__)    


    # filter contact by email and organization.id if it exist
    contact = session.query(Contacts).filter_by(
        email=row['contact_email'],
        organization_id=organization.id
    ).first()

    if contact is None:
        # create a contact instance
        contact = Contacts (
            email=row['contact_email'],
            organization_id=organization.id,
            # set other contact fields
            first_name = row["contact_name"],
            source=row["contact_source"],
            position=row["contact_position"]
        )
        # iff club exist for this contact
        if club is not None: 
            contact.club_id = club.id

        session.add(contact)
        session.commit()
        print(contact.__repr__)

    # filter agent by contact.id and organization.id if it exist
    agent = session.query(Agents).filter_by(
        contact_id=contact.id,
        organization_id=organization.id
    ).first()

    if agent is None:
        # create an agent instance
        agent = Agents (
            rank=row['agent_rank'],
            contact_id=contact.id,
            organization_id=organization.id
        )
        # iff club exist for this agent
        if club is not None: 
            agent.club_id = club.id

        session.add(agent)
        session.commit()
        print(agent.__repr__)


# close connection
session.close()
engine.dispose()
sys.exit(0)

# heroku - create db with appropriate permissions
# config, local migrations
# set up deployments when you push changes to github