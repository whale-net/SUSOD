
import flask
import json
import SUSOD
from SUSOD import util
from SUSOD import model

@SUSOD.app.route('/api/transactions/search', methods=['GET'])
@util.has_permissions
def api_transactions_search():
	# form = util.get_post_json()
	data = model.transactions_search(False)

	context = { 
		**util.get_login_context(),
		**data
	}

	return flask.jsonify(**context)

@SUSOD.app.route('/api/transactions/confirm', methods=['POST'])
@util.has_permissions
def api_transactions_confirm():
	form = util.get_post_json()
	data = model.transactions_confirm(form['SenderReceiver'], form['TransactionID'])

	context = { 
		**util.get_login_context(),
		**data
	}

	return flask.jsonify(**context)
