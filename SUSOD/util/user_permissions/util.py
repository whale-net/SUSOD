"""
Utility functions for handling login permissions.
"""
import flask

from .user import get_UserID

def get_username():
	if 'username' not in flask.session:
		return None
	return flask.session['username']

def is_logged_in():
	return 'Username' in flask.session

def get_login_context():
	context = {
		'Username': get_username(),
		'login_status': is_logged_in(),
		'UserID': get_UserID()
	}
	return context