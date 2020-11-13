
"""
Endpoint for receipts interactions from mobile 

"""

import flask
import json
import SUSOD
from SUSOD import util
from SUSOD import model


@SUSOD.app.route('/mobile/receipts/create', methods=['POST'])
def create_receipt():

	data = json.loads(flask.request.data.decode('utf-8'))

	required_fields = ['OwnerUserID', 'Amount', 'ReceiptTypeID', 'PurchaseDate', 'CreatedBy', 'CreatedDate', 'UpdatedBy', 'UpdatedDate', 'Description', 'UserIdsCommaSeparated']
	optional_fields = [] #store?
	try:
		model.receipt_create(data['OwnerUserID'], data['Amount']
			, data['ReceiptTypeID'], data['PurchaseDate'], data['CreatedBy']
			, data['CreatedDate'], data['UpdatedBy'], data['UpdatedDate'], data['Description']
			, data['UserIdsCommaSeparated'])

		json_data = {"status": 1, "description": "Insert successful"}
		
		return flask.jsonify(json_data)

	except:
		json_data = {"status": 0, "description": 'Insert failed'}
		
		return flask.jsonify(json_data)

@SUSOD.app.route('/api/receipts/setup', methods=['GET'])
@util.has_permissions
def api_receipts_setup():
	form = util.get_post_json()
	data = model.receipts_setup()

	context = { 
		**util.get_login_context(),
		**data
	}

	return flask.jsonify(**context)

@SUSOD.app.route('/api/receipts/search', methods=['POST'])
@util.has_permissions
def api_receipts_search():
	formData = util.get_post_json()
	data = model.receipts_search(formData)

	context = { 
		**util.get_login_context(),
		**data
	}

	return flask.jsonify(**context)


@SUSOD.app.route('/api/receipts/receipt', methods=['POST'])
@util.has_permissions
def api_receipts_receipt():
	formData = util.get_post_json()

	# In this, formData is just our ReceiptID
	data = model.receipts_receipt(formData)

	context = { 
		**util.get_login_context(),
		**data
	}

	return flask.jsonify(**context)

@SUSOD.app.route('/api/receipts/save', methods=['POST'])
@util.has_permissions
def api_receipts_save():
	formData = util.get_post_json()

	data = model.receipts_save(formData)

	context = { 
		**util.get_login_context(),
		**data
	}

	return flask.jsonify(**context)

