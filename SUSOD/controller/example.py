"""
Example endpoint.
"""
import flask
import SUSOD
from SUSOD.model.gimme_data import giveme_data


@SUSOD.app.route('/api/example', methods=["POST"])
def insert_to_test_table():
	"""
	Inserts message into test table.
	"""

	if 'info' in flask.request.form:
		message = flask.request.form['info']
		giveme_data(message)

	return flask.redirect(flask.url_for('show_example_page'))