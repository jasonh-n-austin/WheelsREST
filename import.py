from flask import Flask, g
from flask_peewee.db import MySQLDatabase
from pymongo import MongoClient
import json
import urllib2
import datetime

app = Flask(__name__)
app.config.from_object('config.Configuration')

db = MySQLDatabase('wheels', **app.config['DATABASE'])

#g.db = db
#g.db.connect()

host = 'http://localhost:5000'
def mongo_load(coll, url):
    nextUrl = url
    if coll.count() == 0:
	    while nextUrl:
		response = urllib2.urlopen('%s%s' % (host, nextUrl))
		data = json.load(response)
		nextUrl = data['meta']['next']
		for obj in iter(data['objects']):
		    coll.insert( obj )
    else:
        print str(coll) + ' not empty'

def mongo_import():
    connection = MongoClient()
    connection = MongoClient('localhost', 27017)
    db = connection.wheels_db
    collection = db.wheels_collection

    mongo_load(db.wheelmodels, '/api/wheelmodels')
    mongo_load(db.wheelbrands, '/api/wheelbrands')
    mongo_load(db.wheelspecs, '/api/wheelspecs')
mongo_import()

#g.db.close()
