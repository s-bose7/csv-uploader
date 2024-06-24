import re

from sqlalchemy import desc
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from db.models import Agents, Organizations, Contacts


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


def is_most_recent_contact(session: Session, organization: Organizations, contact: Contacts)->bool:
    if contact is None:
        return False
    # Query the most recent contact for the given organization
    most_recent_contact = session.query(Contacts).filter_by(
        organization_id=organization.id
    ).order_by(desc(Contacts.created_at)).first()
    # Check if the given contact_id is the most recent one
    return most_recent_contact is not None and most_recent_contact.id == contact.id


def update_agent_ranks(session: Session, organization: Organizations)->None:
    # Query all agents associated with the organization
    agents = session.query(Agents).filter_by(organization_id=organization.id).all()
    # Increment the rank of each agent by 1
    for agent in agents:
        agent.rank += 1

    session.commit()