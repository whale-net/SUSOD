"""
User management page
"""
import flask
import SUSOD
from SUSOD import util
from SUSOD import model

@SUSOD.app.route('/api/user/')
@util.has_permissions
def api_user_index():

	login_context = util.get_login_context()

	context = { 
		**login_context,
		**model.user_index_setup(util.get_UserID())
	}

	print(context)
	return flask.jsonify(**context)

