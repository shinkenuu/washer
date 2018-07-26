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

    id = Column(Integer, primary_key=True)
    username = Column(String, index=True)
    password = Column(String)
    able_to_vote = Column(Boolean)
    last_vote_datetime = Column(DateTime, index=True)

    server_id = Column(Integer, ForeignKey('server.id'))


class Server(Base):
    __tablename__ = 'server'

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    host = Column(String)

    credentials = relationship('Credential', backref='server')
