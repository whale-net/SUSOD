"""
JSON and HTTP responses.

Standard set to make some returns hopefully simple?
"""





def http_json_200():
	context = {
		'message': 'OK',
		'status_code': 200
	}
	
	return context