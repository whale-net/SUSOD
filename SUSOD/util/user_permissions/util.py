"""
Utility functions for handling login permissions.
"""
import flask


def get_username():
	if 'username' not in flask.session:
		return None
	return flask.session['username']

def is_logged_in():
	return 'username' in flask.session

def get_login_context():
	context = {
		'username': get_username(),
		'loggin_status': is_logged_in()
	}
	return context