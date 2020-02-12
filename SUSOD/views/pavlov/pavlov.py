#pavlov view
import flask
import SUSOD
from SUSOD import util

@SUSOD.app.route('/pavlov/')
@util.has_permissions
def show_pavlov_index():
	context = util.get_login_context()
	
	return flask.render_template('pavlov/index.html', **context)
