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


def remove_outdated_emails_from_agents(session: Session)->None:
    two_years_ago = datetime.utcnow() - timedelta(days=2*365)
    session.query(Agents).filter(Agents.created_at <= two_years_ago).delete(
        synchronize_session=False
    )
    session.commit()


def remove_agents_with_higher_rank(session: Session)->None:
    session.query(Agents).filter(Agents.rank > 3).delete(synchronize_session=False)