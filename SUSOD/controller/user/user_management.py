"""
User management page
"""
import flask
import SUSOD
from SUSOD import util


@SUSOD.app.route('/api/user/')
@util.has_permissions
def api_user_index():

	context = util.get_login_context()

	return flask.jsonify(**context)

