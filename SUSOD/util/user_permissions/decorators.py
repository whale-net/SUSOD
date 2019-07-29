"""
Decorators for testing if a user is logged in.

Will redirect if a user is not logged in
"""
import flask
import SUSOD

from .util import is_logged_in

def has_permissions(func):
	def wrapper(*args, **kwargs):
		if not is_logged_in():
			flask.abort(403)
		else:
			func(*args, **kwargs)
	return wrapper