import os

from sqlalchemy import (create_engine,
                        Boolean, Column, Integer, String, DateTime, ForeignKey)
from sqlalchemy.orm import (sessionmaker,
                            relationship)
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(os.environ.get('DATABASE_URL', ''))
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()


class Credential(Base):
    __tablename__ = 'credential'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    username = Column(String, index=True, nullable=False)
    password = Column(String, nullable=False)
    able_to_vote = Column(Boolean, index=True, nullable=False)
    last_vote_datetime = Column(DateTime, index=True, nullable=False)

    server_id = Column(Integer, ForeignKey('server.id'), nullable=False)
    server = relationship('Server', backref='credentials')


class Server(Base):
    __tablename__ = 'server'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    host = Column(String, nullable=False)
