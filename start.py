from flask import Flask, Response, request, json
from contextlib import closing
import htmlencode
from response_helper import rh
import wheels_db

app = Flask(__name__)

@app.route('/')
def index():
	return '<a href="/models">Wheels</a>'

@app.route('/brands')
def brands_all():
	def json_item(item):
		return {
			'id'  : item['WheelBrandID'],
			'brand' : htmlencode.html_escape(item['WheelBrandDescription']),
			'url' : htmlencode.html_escape(item['WheelBrandURL']),
			'photo' : htmlencode.html_escape(item['WheelBrandPhotoURL']),
			'notes' : htmlencode.html_escape(item['WheelBrandNotes']),
			'lastUpdated' : htmlencode.html_escape(item['LastUpdated'])
		}

	brand = request.args.get('brand', '')
	if brand == '':
		results = wheels_db.brands_all()
	else: 
		return Response("Brand: "+brand)
	#else:
	#	results = wheels_db.brands_by_brand(brand)	
	return rh.jsonList(results, json_item)

		
@app.route('/models')
def models_all():
	def json_item(item):
		return {
			'id'  : item['WheelModelID'],
			'brand' : htmlencode.html_escape(item['WheelBrandDescription']),
			'name' : htmlencode.html_escape(item['WheelModelDescription'])
		}
	brand = request.args.get('brand', '')
	#if brand == '':
	results = wheels_db.models_all()
	#else:
	#	results = wheels_db.models_by_brand(brand)
	return rh.jsonList(results, json_item)
	
    
@app.route('/models/<int:wheel_model_id>')
def model_by_id(wheel_model_id):
	def json_item(item):
		return {
			'id' : str(item['WheelModelID']),
			'brand' : htmlencode.html_escape(item['WheelBrandDescription']),
			'name' : htmlencode.html_escape(item['WheelModelDescription'])
		}
	results = wheels_db.models_by_id(wheel_model_id)
	data = ''
	if results is None:
		return rh.error("Wheel model " + str(wheel_model_id) + " not found")
	return rh.jsonItem(results, json_item)
    
@app.before_request
def before_request():
	wheels_db.connect()

@app.teardown_request
def teardown_request(exception):
	wheels_db.close()

if __name__ == '__main__':
	app.run(debug=True)
