#transactions view
import flask
import SUSOD
from SUSOD import util

@SUSOD.app.route('/transactions/')
@util.has_permissions
def show_transactions_index():
	context = util.get_login_context()
	
	return flask.render_template('transactions/index.html', **context)
