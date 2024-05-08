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
)

Base = declarative_base()


class Segments(Base):
    __tablename__ = 'segments'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"Segments(id={self.id}, name='{self.name}', created_at='{self.created_at}')"


class Organization(Base):
    __tablename__ = 'organizations'

    id = Column(Integer, primary_key=True)
    segment_id = Column(Integer, ForeignKey('segments.id'))
    name = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    street_address = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    city = Column(String)
    state = Column(String)
    zip = Column(String)
    slug = Column(String)
    category = Column(String)
    custom_fields = Column(JSON)
    irs_ein = Column(String)
    irs_ntee_code = Column(String)
    school_grade = Column(String)
    fall_start_date = Column(DateTime)
    winter_start_date = Column(DateTime)

    # A one-to-many relationship between the Organization and Segment models, 
    # where one Segment can have multiple Organization instances.
    segment = relationship('Segment', backref='organizations')

    def __repr__(self):
        return f"Organization(id={self.id}, name='{self.name}', segment_id={self.segment_id})"
    

class Club(Base):
    __tablename__ = 'clubs'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    organization_id = Column(Integer, ForeignKey('organizations.id'))

    # A one-to-many relationship between the Club and Organization models, 
    # where one Organization can have multiple Club instances.
    organization = relationship('Organization', backref='clubs')

    def __repr__(self):
        return f"Club(id={self.id}, name='{self.name}', organization_id={self.organization_id})"


class Agent(Base):
    __tablename__ = 'agents'

    id = Column(Integer, primary_key=True)
    rank = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    club_id = Column(Integer, ForeignKey('clubs.id'))
    contact_id = Column(Integer, ForeignKey('contacts.id'), unique=True)
    organization_id = Column(Integer, ForeignKey('organizations.id'))

    # A one-to-many relationship between the Agent and Club models, 
    # where one Club can have multiple Agent instances. 
    club = relationship('Club', backref='agents')
    # A one-to-one relationship between the Agent and Contact models, 
    # where one Contact can have at most one Agent instance.
    contact = relationship('Contact', backref='agent', uselist=False)
    # A one-to-many relationship between the Agent and Organization models, 
    # where one Organization can have multiple Agent instances.
    organization = relationship('Organization', backref='agents')

    def __repr__(self):
        return f"Agent(id={self.id}, rank={self.rank}, club_id={self.club_id}, contact_id={self.contact_id}, organization_id={self.organization_id})"
    

class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True)
    email = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    custom_fields = Column(JSON)
    source = Column(String)
    first_name = Column(String)
    position = Column(String)
    organization_id = Column(Integer, ForeignKey('organizations.id'))
    club_id = Column(Integer, ForeignKey('clubs.id'))

    # A one-to-many relationship between the Contact and Organization models,
    # where one Organization can have multiple Contact instances.
    organization = relationship('Organization', backref='contacts')
    # A one-to-many relationship between the Contact and Club models,
    # where one Club can have multiple Contact instances.
    club = relationship('Club', backref='contacts')
    # A one-to-one relationship between the Contact and Agent models,
    # where one agent can have at most one Contact instance. 
    agent = relationship('Agent', backref='contact', uselist=False)

    def __repr__(self):
        return f"Contact(id={self.id}, email='{self.email}', first_name='{self.first_name}', position='{self.position}')"
