"""
Example page.

Used to make sure flask app runs.
"""
import flask
import SUSOD
from SUSOD.util import *

# TODO: move to index module
# this is here for testing right now

@SUSOD.app.route('/')
def show_index():
	""" Display /example page."""

	context = get_login_context()
	
	return flask.render_template('index.html', **context)
