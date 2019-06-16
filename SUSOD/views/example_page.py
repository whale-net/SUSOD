"""
Example page.

Used to make sure flask app runs.
"""
import flask
import SUSOD

from SUSOD.model import get_test_data

@SUSOD.app.route('/example')
def show_example_page():
	""" Display /example page."""

	context = {
		'message': 'Hello World',
		'test_data': get_test_data(),
	}
	
	return flask.render_template('example.html', **context)