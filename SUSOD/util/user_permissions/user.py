"""
Utility functions for handling login permissions.
"""
import flask

def login_user(username):
	# TODO return server error if already logged in?
	flask.session['username'] = username

def logout_user():
	return flask.session.pop('username', None)
	