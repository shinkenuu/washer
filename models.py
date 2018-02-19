from datetime import datetime

from app import db


class Server(db.Model):
    __tablename__ = 'server'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))


class Credential(db.Model):
    __tablename__ = 'credential'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))
    able_to_vote = db.Column(db.Boolean, default=True)
    last_vote_datetime = db.Column(db.DateTime(), default=datetime.utcnow())

    server_id = db.Column(db.Integer, db.ForeignKey('server.id'))
    server = db.relationship('Server', backref='credentials', lazy='dynamic')


class CrawlSpot(db.Model):
    __tablename__ = 'crawl_spot'

    id = db.Column(db.Integer, primary_key=True)
    order_of_crawling = db.Column(db.Integer)
    url = db.Column(db.String(120))

    server_id = db.Column(db.Integer, db.ForeignKey('server.id'))
    server = db.relationship('Server', backref='crawl_spots', lazy='dynamic')


class Form(db.Model):
    __tablename__ = 'form'

    formid = db.Column(db.String(2))
    name = db.Column(db.String(80))
    xpath = db.Column(db.String(80))
    number = db.Column(db.Integer)
    data = db.Column(db.JSON)
    click_data = db.Column(db.JSON)

    spot_id = db.Column(db.Integer, db.ForeignKey('crawl_spot.id'))
    spot = db.relationship('Spot', backref='forms', lazy='dynamic')
