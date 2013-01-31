from flask import Flask, Response, request, json
from contextlib import closing
import htmlencode
import wheels_db

app = Flask(__name__)

@app.route('/')
def index():
	return '<a href="/models">Wheels</a>'

		
@app.route('/models')
def wheel_models_all():
	brand = request.args.get('brand', '')
	if brand is None:
		results = wheels_db.models_all
	else:
		results = wheels_db.models_by_brand(brand)
	
	items = []
	for wheel in results:
		item = {
			'id'  : str(wheel['WheelModelID']),
			'brand' : htmlencode.html_escape(wheel['WheelBrandDescription']),
			'name' : htmlencode.html_escape(wheel['WheelModelDescription'])
		}
		items.append(item)
	data = {
		'items' : items
	}
	
	return Response(json.dumps(data), mimetype='application/json')
    
@app.route('/models/<int:wheel_model_id>')
def wheel_model_by_id(wheel_model_id):
	wheel = wheels_db.models_by_id(wheel_model_id)
	data = ''
	if wheel is None:
		data = '{"error": "Wheel model id does not exist"}'
	else:
		data = {
			'id' : str(wheel['WheelModelID']),
			'brand' : htmlencode.html_escape(wheel['WheelBrandDescription']),
			'name' : htmlencode.html_escape(wheel['WheelModelDescription'])
		}
	return Response(json.dumps(data), mimetype='application/json')
    
@app.before_request
def before_request():
	wheels_db.connect()

@app.teardown_request
def teardown_request(exception):
	wheels_db.close()

if __name__ == '__main__':
	app.run(debug=True)
