import re
from db.models import Agents, Contacts
from datetime import datetime, timedelta

def generate_slug(organization_name:str, address: str)->str:
    combined = organization_name + address
    slug = re.sub(r'[^a-z0-9]+', '-', combined.replace(" ", "").lower()).strip('-')
    return slug


def remove_outdated_emails_from_agents(session):
    two_years_ago = datetime.utcnow() - timedelta(days=2*365)

    # Query for agents created more than or equal to 2 years ago
    outdated_agents = session.query(Agents).filter(Agents.created_at <= two_years_ago).all()
    for agent in outdated_agents:
        # Find and remove association to the associated contacts
        session.query(Agents).filter(Agents.id == agent.id).update({"contact_id": None})
    
    # Delete the outdated agents
    session.query(Agents).filter(Agents.created_at <= two_years_ago).delete(synchronize_session=False)

    session.commit()
