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

    def __iter__(self):
        columns = ['id', 'username', 'password', 'able_to_vote', 'last_vote_datetime', 'server_id']
        for column in columns:
            yield (column, self.__getattribute__(column))


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
            return self

        columns = ['formid', 'name', 'xpath', 'number', 'data', 'click_data']

        # --------- Copy self without sqlalchemy attrs ----------------------
        # ---------------------------------------------------------------------
        interpreted_form = CrawlForm()
        for column in columns:
            interpreted_form.__setattr__(column, self.__getattribute__(column))
        # ---------------------------------------------------------------------

        for static_key, dynamic_value in kwargs.items():
            dunder_static_key = '__' + static_key + '__'

            for column in columns:
                if not interpreted_form.__getattribute__(column):
                    continue

                column_value = interpreted_form.__getattribute__(column)

                if isinstance(column_value, str):
                    if dunder_static_key in column_value:
                        interpreted_form.__setattr__(
                            column,
                            eval(column_value.replace(dunder_static_key, 'dynamic_value')))

                elif isinstance(column_value, dict):
                    interpreted_dict = {}

                    for key, value in column_value.items():
                        interpreted_key = key
                        interpreted_value = value

                        if isinstance(key, str) and dunder_static_key in key:
                            interpreted_key = eval(key.replace(dunder_static_key, 'dynamic_value'))

                        if isinstance(value, str) and dunder_static_key in value:
                            interpreted_value = eval(value.replace(dunder_static_key, 'dynamic_value'))

                        interpreted_dict[interpreted_key] = interpreted_value

                    interpreted_form.__setattr__(column, interpreted_dict)

        return interpreted_form

    def to_scrapy_form(self, **kwargs):
        """
        Parse values into scrapy.FormRequest arguments
        """
        interpreted_form = self.interpret(**kwargs)

        return {
            'formid': interpreted_form.formid,
            'formname': interpreted_form.name,
            'formxpath': interpreted_form.xpath,
            'formnumber': interpreted_form.number,
            'formdata': interpreted_form.data,
            'clickdata': interpreted_form.click_data
        }
