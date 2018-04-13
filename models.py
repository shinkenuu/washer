from datetime import datetime, timedelta

from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Server(Base):
    __tablename__ = 'server'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    base_url = Column(String(40), nullable=False)
    last_vote_datetime = Column(DateTime(), nullable=False, default=datetime.utcnow())

    @property
    def all_able_to_vote_credentials(self):
        return [credential for credential in self.credentials if credential.able_to_vote]

    @property
    def all_credentials_available_to_vote(self):
        return sorted(
            [c for c in self.all_able_to_vote_credentials
             if datetime.utcnow() > c.last_vote_datetime + timedelta(hours=12)],
            key=lambda c: c.last_vote_datetime)


class Credential(Base):
    __tablename__ = 'credential'

    id = Column(Integer, primary_key=True)
    username = Column(String(30), nullable=False)
    password = Column(String(30), nullable=False)
    able_to_vote = Column(Boolean, nullable=False, default=False)
    last_vote_datetime = Column(DateTime(), nullable=False, default=datetime.utcnow())

    server_id = Column(Integer, ForeignKey('server.id'), nullable=False)
    server = relationship('Server', backref='credentials')

    def serialize(self):
        return str(
            {
                'username': self.username,
                'able_to_vote': 'true' if self.able_to_vote else 'false',
                'last_vote_datetime': self.last_vote_datetime.strftime('yyyy-MM-dd'),
                'server': self.server.name
            }
        )
