"""
Example page.

Used to make sure flask app runs.
"""
import flask
import SUSOD

@SUSOD.app.route('/example')
def show_example_page():
	""" Display /example page."""

	context = {
		'message': 'Hello World',
	}
	
	return flask.render_template('example.html', **context)