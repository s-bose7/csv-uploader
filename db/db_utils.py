import re

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from db.models import Agents
from datetime import datetime, timedelta


def add_and_commit(session: Session, new_record)->None:
    try:
        session.add(new_record)
        session.commit()
        print(new_record.__repr__())
    except SQLAlchemyError as e:
        session.rollback()
        print(f"An error occurred: {e}")


def generate_slug(organization_name:str, address: str)->str:
    if not isinstance(organization_name, str):
        organization_name = str(organization_name)
    if not isinstance(address, str):
        address = str(address)

    combined = organization_name + address
    slug = re.sub(r'[^a-z0-9]+', '-', combined.replace(" ", "").lower()).strip('-')
    return slug


def remove_outdated_emails_from_agents(session: Session):
    two_years_ago = datetime.utcnow() - timedelta(days=2*365)

    # Query for agents created more than or equal to 2 years ago
    outdated_agents = session.query(Agents).filter(Agents.created_at <= two_years_ago).all()
    for agent in outdated_agents:
        # Find and remove association to the associated contacts
        session.query(Agents).filter(Agents.id == agent.id).update({"contact_id": None})
    # Delete the outdated agents
    session.query(Agents).filter(Agents.created_at <= two_years_ago).delete(synchronize_session=False)

    session.commit()