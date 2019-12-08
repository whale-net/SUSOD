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


	"""
 	creates receords in ReceiptsUsers for this receipt
	"""
	if receipt_id == 0:
		raise
	sql = """
		
		"""
	return




