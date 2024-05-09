# Orchestrate the data migration process.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.models import (
    Segments,
    Organizations,
    Clubs,
    Agents,
    Contacts,
)

from utils.csv_utils import read_file, validate_data

HOST = "localhost"
PORT = 5432
IMAGE_NAME = "postgres"
PASSWORD = "bose1234"
DATABASE_NAME = "group_contacts"
FILE_PATH = "data/csv_files/group_contacts.csv"

# read raw input
data = read_file(file_path=FILE_PATH)
# transform and validate raw input
validated_data = validate_data(data)

# connect to database engine
engine = create_engine(f"postgresql://{IMAGE_NAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}")
Session = sessionmaker(bind=engine)
session = Session()

# insert data
for index, row in validated_data.iterrows():
    
    segment = session.query(Segments).filter_by(name=row['segment_name']).first()
    if segment is None:
        # Create a Segment instance
        segment = Segments(name=row['segment_name'])
        session.add(segment)
        session.commit()
        print(segment.__repr__)

    # secondary identifier for organization
    slug = str(row['organization_name'] + str(row['address'])).replace(" ", "").lower()
    
    organization = session.query(Organizations).filter_by(slug=slug, segment_id=segment.id).first()
    if organization is None:
        # Create an Organization instance
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
            category=row['organization_category'],
            # Set other org fields
            irs_ein = row["irs_ein"],
            irs_ntee_code=row["irs_ntee_code"],
            school_grade=row["school_grade"],
            # fall_start_date=row["fall_start_date"],
            # winter_start_date=row["winter_start_date"],
        )
        session.add(organization)
        session.commit()
        print(organization.__repr__)


    # club = session.query(Clubs).filter_by(name=row['club_name'], organization_id=organization.id).first()
    # if club is None:
    #     # Create a Club instance
    #     club = Clubs(name=row['club_name'], organization_id=organization.id)
    #     session.add(club)
    #     session.commit()
    #     print(club.__repr__)    


    contact = session.query(Contacts).filter_by(email=row['contact_email']).first()
    if contact is None:
        # Create a Contact instance
        contact = Contacts (
            email=row['contact_email'],
            organization_id=organization.id,
            # club_id=club.id,
            # Set other contact fields
            source=row["contact_source"],
            # first_name=row["first_name"],
            position=row["contact_position"]
        )
        session.add(contact)
        session.commit()
        print(contact.__repr__)


    agent = session.query(Agents).filter_by(contact_id=contact.id).first()
    if agent is None:
        # Create an Agent instance
        agent = Agents (
            rank=row['agent_rank'],
            # club_id=club.id,
            contact_id=contact.id,
            organization_id=organization.id
        )
        session.add(agent)
        session.commit()
        print(agent.__repr__)


# close connection
session.close()
engine.dispose()
exit(0)