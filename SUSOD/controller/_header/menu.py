"""
functions for creating menu
"""
import flask
import SUSOD
from SUSOD import util
from SUSOD import model


@SUSOD.app.route('/api/_header/', methods=['GET'])
@util.has_permissions
def api__header_get_menu_options():
	"""
	Return json string of menu options
	"""
	context = {
		'menu': model.get_menu_options()
	}
	
	
	return flask.jsonify(**context)