from flask import Response, json

class rh:
	@staticmethod
	def jsonList(results, json_item):
		if results is None:
			return errorOutput("Results are empty")
		items = []
		for item in results:
			items.append(json_item(item))
		output = { 'items' : items }
		return Response(json.dumps(output), mimetype='application/json')

	@staticmethod
	def jsonItem(item, json_item):
		output = json_item(item)
		return Response(json.dumps(output), mimetype='application/json')

	@staticmethod
	def error(message):
		output = { "error" : message }
		return Response(json.dumps(output), mimetype='application/json')