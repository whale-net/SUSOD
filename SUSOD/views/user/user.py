"""
User view.
"""
import flask
import SUSOD
from SUSOD import util

@SUSOD.app.route('/user/login')
def show_user_login():
	""" Display /example page."""

	context = util.get_login_context()
	
	return flask.render_template('user/login.html', **context)

@SUSOD.app.route('/user/create')
def show_user_create():
	""" Display /example page."""

	context = util.get_login_context()
	
	return flask.render_template('user/create.html', **context)

@SUSOD.app.route('/user/')
def show_user_index():
	""" Display /example page."""

	context = util.get_login_context()


	
	return flask.render_template('user/index.html', **context)