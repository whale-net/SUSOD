"""
Login endpoint.
"""
import flask
import SUSOD

from SUSOD.util import *

# todo import model functions

@SUSOD.app.route('/api/login', methods=["GET"])
def api_login():
	"""
	Handles login POST request.

	Will setup the user's flask header.
	"""

	print(password_db_string_create("hello"))
	return ""
	# return flask.redirect(flask.url_for('show_example_page'))