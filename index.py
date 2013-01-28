from flask import Flask, Response, request, g
import sqlite3
from contextlib import closing
import htmlencode

app = Flask(__name__)

DATABASE = 'wheels.db'

def connect_db():
	return sqlite3.connect(DATABASE)

def query_db(query, args=(), one=False):
	cur = g.db.execute(query, args)
	rv = [dict((cur.description[idx][0], value)
			for idx, value in enumerate(row)) for row in cur.fetchall()]
	return (rv[0] if rv else None) if one else rv

@app.route('/')
def index():
	return '<a href="/wheelmodels">Wheels</a>'

WHEEL_QUERY = '''
		select wb.WheelBrandID, wb.WheelBrandDescription, wm.WheelModelID, 
		wm.WheelModelDescription 
		from wheelmodels wm 
		inner join wheelbrands wb on wm.WheelBrandID = wb.WheelBrandID
		'''
		
@app.route('/wheelmodels')
def wheel_models_all():
	brand = request.args.get('brand', '')
	ret = '{ "items": [\n'
	query = WHEEL_QUERY
	if brand is None:
		results = query_db(query)
	else:
		query += "where wb.WheelBrandDescription = ?" 
		results = query_db(query, (brand,))
	for wheel in results:
		ret += '{\n"id": "' + str(wheel['WheelModelID']) + '", \n'
		ret += '"brand": "' + str(wheel['WheelBrandDescription']) + '", \n'
		ret += '"name": "' + htmlencode.html_escape(wheel['WheelModelDescription']) + '"\n},'
	ret = ret[0:-1] #strip off the trailing comma
	ret += ']}'
	return Response(ret, mimetype='application/json')
    
@app.route('/wheelmodels/<int:wheel_model_id>')
def wheel_model_by_id(wheel_model_id):
	wheel = query_db(WHEEL_QUERY+' where wm.WheelModelID = ?', (wheel_model_id, ), one=True)
	ret = ''
	if wheel is None:
		ret = '{"error": "Wheel model id does not exist"}'
	else:
		ret += '{\n"id": "' + str(wheel['WheelModelID']) + '", \n'
		ret += '"brand": "' + str(wheel['WheelBrandDescription']) + '", \n'
		ret += '"name": "' + htmlencode.html_escape(wheel['WheelModelDescription']) + '"\n}'
	return Response(ret, mimetype='application/json')
    
@app.before_request
def before_request():
	g.db = connect_db()
	#init_db()

@app.teardown_request
def teardown_request(exception):
	if hasattr(g, 'db'):
		g.db.close()


if __name__ == '__main__':
	app.run(debug=True)
