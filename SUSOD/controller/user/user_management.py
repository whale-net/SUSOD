"""
User management page
"""
import flask
import SUSOD
from SUSOD import util
from SUSOD import model

@SUSOD.app.route('/api/user/', methods=['GET'])
@util.has_permissions
def api_user_index():

	login_context = util.get_login_context()

	context = { 
		**login_context,
		**model.user_index_setup(util.get_UserID())
	}

	return flask.jsonify(**context)

@SUSOD.app.route('/api/user/', methods=['POST'])
@util.has_permissions
def api_user_index_update():
	form = util.get_post_json()
	model.user_index_update(util.get_UserID(), form)

	context = { 
		**util.get_login_context(),
		**model.user_index_setup(util.get_UserID())
	}

	return flask.jsonify(**context)

