"""
Login endpoint.
"""
import flask
import SUSOD
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
		return flask.redirect(flask.url_for('show_user_login')),401

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

