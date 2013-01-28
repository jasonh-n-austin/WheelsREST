from flask import Flask
from flask import g
import sqlite3
from contextlib import closing

DATABASE = 'wheels.db'

app = Flask(__name__)

def connect_db():
	return sqlite3.connect(DATABASE)

def init_db():
    with closing(connect_db()) as db:
		with app.open_resource('schema.sql') as f:
			db.cursor().executescript(f.read())
		db.commit()

def query_db(query, args=(), one=False):
	cur = g.db.execute(query, args)
	rv = [dict((cur.description[idx][0], value)
			for idx, value in enumerate(row)) for row in cur.fetchall()]
	return (rv[0] if rv else None) if one else rv

@app.route('/')
def index():
	return '<a href="/wheelmodels">Wheels</a>'

@app.route('/wheelmodels')
def wheel_models_all():
	ret = ""
	for user in query_db('select * from wheelmodels'):
		ret += user['name'], 'has the id', user['wheelmodelid']
	return ret
    
@app.route('/wheelmodels/<int:wheel_model_id>')
def wheel_model_by_id(wheel_model_id):
	user = query_db('select * from wheelmodels where wheelmodelid = ?', wheel_model_id, one=True)
	if user is None:
		print 'Wheel does not exist'
	else:
		print wheel_model_id, 'has the name', user['name']
    
@app.before_request
def before_request():
	g.db = connect_db()
	init_db()

@app.teardown_request
def teardown_request(exception):
	if hasattr(g, 'db'):
		g.db.close()


if __name__ == '__main__':
	app.run(debug=True)
