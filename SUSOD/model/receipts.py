import flask
import SUSOD
from SUSOD import util

from .db import *


def receipt_create(OwnerUserID, Amount, ReceiptTypeID, PurchaseDate, CreatedBy, CreatedDate, UpdatedBy, UpdatedDate, Description, UserIdsCommaSeparated):
	"""
	creates receipt in db
	"""
	receipt_id = 0

	cursor = get_db().cursor()
	sql = """
		INSERT INTO Receipts(OwnerUserID, Amount, ReceiptTypeID, PurchaseDate, CreatedBy, CreatedDate, UpdatedBy, UpdatedDate, Description)
		VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
		"""

	try:
		cursor.execute(sql, (OwnerUserID, Amount, ReceiptTypeID, PurchaseDate, CreatedBy, CreatedDate, UpdatedBy, UpdatedDate, Description))
	
		receipt_id = cursor.lastrowid
	except:
		raise


	sql_params = []
	cursor = get_db().cursor()
	user_ids = UserIdsCommaSeparated.split(',')
	sql = """
		INSERT INTO ReceiptsUsers(ReceiptID, UserID, PaymentRatio, DeductionAmount, CreatedBy, CreatedDate, UpdatedBy, UpdatedDate) 
		VALUES
	""".strip() + " "
	for user_id in user_ids: 
		sql += """
			( %s, %s, %s, %s, %s, %s, %s, %s ),
			
		""".strip() + " "
		sql_params += [receipt_id, int(user_id), 1, 0, 9, CreatedDate, 9, UpdatedDate]

	sql = sql[:-2] + ";" #remove last comma

	try:
		cursor.execute(sql, tuple(sql_params))
	except Exception as e:
		print(str(e))
		raise
