"""
functions for creating menu
"""
import flask
import SUSOD
import json

from SUSOD.util import has_permissions
from SUSOD.model import model_get_menu_options

@SUSOD.app.route('/api/_header/', methods=['GET'])
@has_permissions
def api__header_get_menu_options():
	"""
	Return json string of menu options
	"""
	context = model_get_menu_options()
	
	
	return json.dumps(context)