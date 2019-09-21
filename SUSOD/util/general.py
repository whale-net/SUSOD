

import flask
import SUSOD
import json

def get_post_json():
	if not flask.request:
		return
	if not flask.request.method == 'POST':
		return
	
	return json.loads(flask.request.data.decode("utf-8"))

