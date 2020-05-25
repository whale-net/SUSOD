import flask
import SUSOD
from SUSOD import util
from SUSOD import config

from .db import *
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, MetaData, Table
from sqlalchemy.orm import sessionmaker

#Base class definition for sqlalchemy classes
Base = declarative_base()

#Model class
class Receipt(Base):
	__tablename__ = 'Receipts'

	ReceiptID = Column(Integer, primary_key=True)
	Description = Column(String)
	Amount = Column(Float)

	def __repr__(self):
		return "<Receipt(ReceiptID='%s', Description='%s', Amount='%s')>" % (self.ReceiptID, self.Description, self.Amount)


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



def receipts_setup():
	engine = create_engine('mysql+pymysql://'+config.DATABASE_USERNAME+':'+config.DATABASE_PASSWORD+'@'+config.DATABASE_HOSTNAME+'/'+config.DATABASE_NAME, echo=True)
	Session = sessionmaker(bind=engine)

	session = Session()
	
	for i in session.query(Receipt):
		print(i)
		
	print(session)

def receipts_search(formData):
	engine = create_engine('mysql+pymysql://'+config.DATABASE_USERNAME+':'+config.DATABASE_PASSWORD+'@'+config.DATABASE_HOSTNAME+'/'+config.DATABASE_NAME, echo=True)

	Session = sessionmaker(bind=engine)
	session = Session()
	
	qry = session.query(Receipt)

	if (formData['Description'] != ''):
		qry.filter(Receipt.Description.like('%' + '%s' + '%', tuple(formData["Description"])))


	returnSet = {'data': []}
	for i in session.query(Receipt):
		returnSet['data'] += [{'ReceiptID': i.ReceiptID, 'Description': i.Description, 'Amount': i.Amount}]


	return returnSet