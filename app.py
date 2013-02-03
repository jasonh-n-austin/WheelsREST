from flask import Flask, g
from flask_peewee.db import MySQLDatabase
#from models import User

app = Flask(__name__)
app.config.from_object('config.Configuration')

#db = MySQLDatabase(app.config['DATABASE'])
db = MySQLDatabase('rafarafi_wheels', **{'passwd': 'ktd#433', 'host': 'pragmaticapi.com', 'user': 'rafarafi_admin'})

@app.before_request
def before_request():
    g.db = db
    g.db.connect()

@app.after_request
def after_request(response):
    g.db.close()
    return response