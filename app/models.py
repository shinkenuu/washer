from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship

from app.database import Base


class Server(Base):
    __tablename__ = 'server'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)

    @property
    def next_to_vote(self):
        return min([c for c in self.credentials if c.able_to_vote],
                   key=lambda credential: credential.last_vote_datetime)


class Credential(Base):
    __tablename__ = 'credential'

    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True, nullable=False)
    password = Column(String(30), nullable=False)
    able_to_vote = Column(Boolean, nullable=False, default=True)
    last_vote_datetime = Column(DateTime(), nullable=False, default=datetime.utcnow())

    server_id = Column(Integer, ForeignKey('server.id'), nullable=False)
    server = relationship('Server', backref='credentials')


class CrawlSpot(Base):
    __tablename__ = 'crawl_spot'

    id = Column(Integer, primary_key=True)
    order_of_crawling = Column(Integer, nullable=False)
    url = Column(String(120), nullable=False)

    server_id = Column(Integer, ForeignKey('server.id'), nullable=False)
    server = relationship('Server', backref='crawl_spots')


class CrawlForm(Base):
    __tablename__ = 'crawl_form'

    id = Column(Integer, primary_key=True)
    formid = Column(String(2))
    name = Column(String(80))
    xpath = Column(String(80))
    number = Column(Integer)
    data = Column(JSON)
    click_data = Column(JSON)

    spot_id = Column(Integer, ForeignKey('crawl_spot.id'), nullable=False)
    spot = relationship('CrawlSpot', backref='forms')

    def interpret(self, **kwargs):
        """
        Change static formatted values into dynamic.

        i.e: click_data = {username = __crendential__.username} -> {username = kwargs['credential'].username}
        :param kwargs: static_value: dynamic_value. i.e credential: instance of Credential
        :return: the interpreted form
        """
        if not kwargs:
            raise KeyError

        interpreted_form = CrawlForm()

        columns = ['formid', 'name', 'xpath', 'number', 'data', 'click_data']

        for static_key, dynamic_value in kwargs.items():
            dunder_static_key = '__' + static_key + '__'

            for column in columns:

                if dunder_static_key in self.__getattribute__(column):
                    interpreted_form.__setattr__(
                        column,
                        eval(self.column.replace(dunder_static_key, str(dynamic_value))))

        return interpreted_form

    @property
    def to_scrapy_form(self):
        """
        Parse values into scrapy.FormRequest arguments
        """
        interpreted_form = self.interpret()

        return {
            'formid': interpreted_form.formid,
            'formname': interpreted_form.name,
            'formxpath': interpreted_form.xpath,
            'formnumber': interpreted_form.number,
            'formdata': interpreted_form.data,
            'clickdata': interpreted_form.click_data
        }
