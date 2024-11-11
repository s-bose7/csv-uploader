from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    JSON,
    Column, 
    Integer, 
    Float,
    String, 
    TIMESTAMP,
    DateTime,
    ForeignKey,
    Boolean
)
from geoalchemy2 import Geometry

Base = declarative_base()


class Organizations(Base):
    __tablename__ = 'organizations'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime, onupdate=func.now())
    street_address = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    geom = Column(Geometry(geometry_type='POINT', srid=4326))
    city = Column(String)
    state = Column(String)
    zip = Column(String)
    slug = Column(String, nullable=False)
    category = Column(String)
    custom_fields = Column(JSON, nullable=True)

    def __repr__(self):
        return f"Organization(id={self.id}, name='{self.name}', category={self.category})"
    

class Clubs(Base):
    __tablename__ = 'clubs'

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey('organizations.id'), nullable=False)
    name = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    # A one-to-many relationship between the Club and Organization models, 
    # where one Organization can have multiple Club instances.
    organization = relationship('Organizations', backref='clubs')

    def __repr__(self):
        return f"Club(id={self.id}, name='{self.name}', organization_id={self.organization_id})"


class Agents(Base):
    __tablename__ = 'agents'

    id = Column(Integer, primary_key=True)
    club_id = Column(Integer, ForeignKey('clubs.id'))
    contact_id = Column(Integer, ForeignKey('contacts.id'), unique=True, nullable=False)
    organization_id = Column(Integer, ForeignKey('organizations.id'), nullable=False)
    rank = Column(Integer)
    segment_name = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    # A one-to-many relationship between the Agent and Club models, 
    # where one Club can have multiple Agent instances. 
    club = relationship('Clubs', backref='agents')
    # A one-to-one relationship between the Agent and Contact models, 
    # where one Contact can have at most one Agent instance.
    contact = relationship('Contacts', backref='agents', uselist=False)
    # A one-to-many relationship between the Agent and Organization models, 
    # where one Organization can have multiple Agent instances.
    organization = relationship('Organizations', backref='agents')

    def __repr__(self):
        return f"Agent(id={self.id}, rank={self.rank}, organization_id={self.organization_id})"
    

class Contacts(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    organization_id = Column(Integer, ForeignKey('organizations.id'), nullable=False)
    club_id = Column(Integer, ForeignKey('clubs.id'))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    project_source = Column(String, nullable=True)
    marketability = Column(Boolean, nullable=True)
    custom_fields = Column(JSON, nullable=True)

    # A one-to-many relationship between the Contact and Organization models,
    # where one Organization can have multiple Contact instances.
    organization = relationship('Organizations', backref='contacts')
    # A one-to-many relationship between the Contact and Club models,
    # where one Club can have multiple Contact instances.
    club = relationship('Clubs', backref='contacts')

    def __repr__(self):
        return f"Contact(id={self.id}, email='{self.email}', organization_id={self.organization_id}')"
