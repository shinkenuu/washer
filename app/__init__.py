from os import environ

from flask import Flask, jsonify

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Build the database:
# This will create the database file using SQLAlchemy

#db.create_all()
from app import database
database.init_db()

from app.views import *

@app.errorhandler(404)
def page_not_found(e):
    return jsonify(error=404, text='Resource not found'), 404