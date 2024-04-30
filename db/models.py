
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column, 
    Integer, 
    String, 
    TIMESTAMP
)

Base = declarative_base()


class Segments(Base):
    __tablename__ = 'segments'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    created_at = Column(TIMESTAMP)

    def __repr__(self):
        return f"Segments(id={self.id}, name='{self.name}', created_at='{self.created_at}')"