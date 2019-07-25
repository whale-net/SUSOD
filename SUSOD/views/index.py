"""
Example page.

Used to make sure flask app runs.
"""
import flask
import SUSOD

@SUSOD.app.route('/')
def show_index():
	""" Display /example page."""

	context = {}
	
	return flask.render_template('index.html', **context)