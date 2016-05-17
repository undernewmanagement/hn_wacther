from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, create_engine
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

import os


Base = declarative_base()

class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True)
    url = Column(String)
    title = Column(String)
    domain = Column(String) # add index=True if you want an index
    user = Column(String)
    created_at = Column(DateTime, default=func.now())

    snapshots = relationship("Snapshot", back_populates="link", cascade="all, delete, delete-orphan")

    def __repr__(self):
        return "<Link(id='{}', url='{}'>".format(self.id, self.url)

class Snapshot(Base):
    __tablename__ = "snapshots"

    id = Column(Integer, primary_key=True)
    link_id = Column(Integer, ForeignKey('links.id'))
    position = Column(Integer)
    points = Column(Integer)
    comments = Column(Integer)
    created_at = Column(DateTime, default=func.now())

    link = relationship("Link", back_populates="snapshots")
    
    def __repr__(self):
        return "<Snapshot(id='{}', link_id='{}'>".format(self.id, self.link_id)



# export DB_URL=postgresql://dn_user:db_pass@db_host/db_name
db_url = os.getenv('DB_URL')
engine = create_engine(db_url)
Base.metadata.create_all(engine)

