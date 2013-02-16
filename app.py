from flask import Flask, g
from flask_peewee.db import MySQLDatabase
#from models import User

app = Flask(__name__)
app.config.from_object('config.Configuration')

db = MySQLDatabase('wheels', **app.config['DATABASE'])

@app.route("/mongoimport")
def mongo_import():
    connection = MongoClient()
    connection = MongoClient('localhost', 27017)
    db = connection.wheels_db
    collection = db.wheels_collection
    wheels = db.wheels
#    f = urllib2.urlopen('http://localhost:5000/api/wheelbrands')
#    json = simplejson.load(f)
#    wheels.insert({"id":1,"description":"Blah"})

@app.before_request
def before_request():
    g.db = db
    g.db.connect()

@app.after_request
def after_request(response):
    g.db.close()
    return response
