from flask import Flask, g
from flask_peewee.db import MySQLDatabase
#from models import User

app = Flask(__name__)
app.config.from_object('config.Configuration')

db = MySQLDatabase('wheels', **app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = db
    g.db.connect()

@app.after_request
def after_request(response):
    g.db.close()
    return response
