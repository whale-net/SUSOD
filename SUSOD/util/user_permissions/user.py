"""
Utility functions for handling login permissions.
"""
import flask

def login_user(UserID, Username):
	# TODO return server error if already logged in?
	flask.session['UserID'] = UserID
	flask.session['Username'] = Username

def logout_user():
	return flask.session.pop('Username', None)
	
def get_UserID():
	return flask.session['UserID']