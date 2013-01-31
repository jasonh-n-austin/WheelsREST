from flask import Flask, Response, request
from contextlib import closing
import htmlencode
import wheels_db

app = Flask(__name__)

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
		results = wheels_db.query_db(query)
	else:
		query += "where wb.WheelBrandDescription = ?" 
		results = wheels_db.query_db(query, (brand,))
	for wheel in results:
		ret += '{\n"id": "' + str(wheel['WheelModelID']) + '", \n'
		ret += '"brand": "' + str(wheel['WheelBrandDescription']) + '", \n'
		ret += '"name": "' + htmlencode.html_escape(wheel['WheelModelDescription']) + '"\n},'
	ret = ret[0:-1] #strip off the trailing comma
	ret += ']}'
	return Response(ret, mimetype='application/json')
    
@app.route('/wheelmodels/<int:wheel_model_id>')
def wheel_model_by_id(wheel_model_id):
	wheel = wheels_db.query_db(WHEEL_QUERY+' where wm.WheelModelID = ?', (wheel_model_id, ), one=True)
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
	wheels_db.connect()

@app.teardown_request
def teardown_request(exception):
	wheels_db.close()

if __name__ == '__main__':
	app.run(debug=True)
