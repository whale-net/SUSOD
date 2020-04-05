"""
Login endpoint.
"""
import flask
import SUSOD
import json
from SUSOD import util
from SUSOD import model


# TODO better logic handling on bad login

@SUSOD.app.route('/api/user/login', methods=['POST'])
def api_user_login():
    """
	Handles login POST request.

	Will setup the user's flask header.
	"""
    form = flask.request.form

    if util.is_logged_in():
        return flask.redirect(flask.url_for('show_index'))

    if 'username' not in form or 'password' not in form:
        return flask.redirect(flask.url_for('show_user_login'))
    try:
        model.user_login(form['username'], form['password'])
    except:
        return flask.redirect(flask.url_for('show_user_login')), 401

    return flask.redirect(flask.url_for('show_index'))


@SUSOD.app.route('/api/user/create', methods=['POST'])
def api_user_create():
    """
	Handles create POST request.

	Will setup the user's flask header.
	"""
    form = flask.request.form

    if 'username' not in form or 'password1' not in form or 'password2' not in form:
        return flask.redirect(flask.url_for('show_user_login'))

    model.user_create(form['username'], form['password1'], form['password2'])

    return flask.redirect(flask.url_for('show_index'))


@SUSOD.app.route('/api/user/logout', methods=['GET'])
def api_user_logout():
    """
	Handles logout GET request.

	Will setup the user's flask header.
	"""
    # TODO make POST enabled once logout button exists...

    util.logout_user()

    return flask.redirect(flask.url_for('show_user_login'))


@SUSOD.app.route('/mobile/user/login', methods=['POST'])
def mobile_user_login():
    json_data = flask.request.data.decode('utf-8')
    print(json_data)

    data = json.loads(json_data)

    if 'username' not in data or 'password' not in data:
        json_data = {"status": 0, "description": "Username or password not set"}

        return flask.jsonify(json_data)
    try:
        user_id = model.user_login_return_id(data['username'], data['password'])
        json_data = {"status": user_id, "description": "Sign in successful"}

        return flask.jsonify(json_data)

    except:
        json_data = {"status": 0, "description": "Username or password incorrect"}

        return flask.jsonify(json_data)