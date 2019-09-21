"""
Decorators for testing if a user is logged in.

Will redirect if a user is not logged in
"""
import flask
import SUSOD
from functools import wraps

from .util import is_logged_in

def has_permissions(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		if not is_logged_in():
			return flask.redirect(flask.url_for('show_user_login')), 401
			# return flask.abort(403)
		else:
			return func(*args, **kwargs)
	return wrapper