"""
Security view.
"""
import flask
import SUSOD
from SUSOD import util

@SUSOD.app.route('/security/')
@util.has_permissions
def show_security_index():
	""" Display /example page."""

	context = util.get_login_context()
	
	return flask.render_template('security/index.html', **context)
