"""
User management page
"""
import flask
import SUSOD
from SUSOD import util
from SUSOD import model
from SUSOD.model import Entity

@SUSOD.app.route('/api/user/', methods=['GET'])
@util.has_permissions
def api_user_index():

	login_context = util.get_login_context()

	data = model.user_index_setup(util.get_UserID())
	data['avatar_url'] = f'/api/entity/{data["AvatarEntityID"]}'

	context = { 
		**login_context,
		**data
	}

	model.get_file(1)

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

@SUSOD.app.route('/api/user/avatar', methods=['POST'])
@util.has_permissions
def api_user_avatar_update():
	file = flask.request.files['file']

	entity = model.Entity()
	entity.create(file)
	model.user_update_avatar(util.get_UserID(), entity.EntityID)

	return util.http_json_200()