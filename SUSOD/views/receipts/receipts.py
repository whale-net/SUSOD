#receipts view
import flask
import SUSOD
from SUSOD import util

@SUSOD.app.route('/receipts/')
@util.has_permissions
def show_receipts_index():
	context = util.get_login_context()
	
	return flask.render_template('receipts/index.html', **context)
