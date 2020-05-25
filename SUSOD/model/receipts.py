import flask
import SUSOD
from SUSOD import util
from SUSOD import config

from .db import *
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, MetaData, Table, join, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker

#Base class definition for sqlalchemy classes
Base = declarative_base()

#Model class
# class Receipts(Base):
# 	__tablename__ = 'Receipts'

# 	ReceiptID = Column(Integer, primary_key=True)
# 	Description = Column(String)
# 	Amount = Column(Float)
# 	PurchaseDate = Column(DateTime)
# 	OwnerUserID = Column(Integer, ForeignKey('Users.UserID'))

# 	def __repr__(self):
# 		return "<Receipts(ReceiptID='%s', Description='%s', Amount='%s')>" % (self.ReceiptID, self.Description, self.Amount)

# class ReceiptsUsers(Base):
# 	__tablename__ = 'ReceiptsUsers'

# 	ReceiptUserID = Column(Integer, primary_key=True)
# 	ReceiptID = Column(Integer, ForeignKey('Receipts.ReceiptID'))
# 	UserID = Column(Integer, ForeignKey('Users.UserID'))

# 	def __repr__(self):
# 		return "<ReceiptsUsers(ReceiptUserID='%s', ReceiptID='%s')>" % (self.ReceiptUserID, self.ReceiptID)

# class Users(Base):
# 	__tablename__ = 'Users'

# 	UserID = Column(Integer, primary_key=True)
# 	Username = Column(String)

# 	def __repr__(self):
# 		return "<Users(UserID='%s', Username='%s')>" % (self.UserID, self.Username)


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
	
	for i in session.query(Receipts):
		print(i)
		
	print(session)

def receipts_search(formData):
	engine = create_engine('mysql+pymysql://'+config.DATABASE_USERNAME+':'+config.DATABASE_PASSWORD+'@'+config.DATABASE_HOSTNAME+'/'+config.DATABASE_NAME, echo=True)

	Session = sessionmaker(bind=engine)
	session = Session()
	

	meta = MetaData()
	meta.reflect(bind=engine)

	# receipts = Table('Receipts', meta, autoload=True, autoload_with=engine)
	# users = Table('Users', meta, autoload=True, autoload_with=engine)
	receipts = meta.tables["Receipts"]
	users = meta.tables["Users"]

	returnSet = {'data': []}
	for r in session\
			.query(receipts, users)\
			.join( receipts, receipts.c['OwnerUserID'] == users.c["UserID"])\
			.order_by(receipts.c['ReceiptID']):
			# .query(receipts, users)\
			# .join(users, receipts.OwnerUserID == users.UserID)\
			# .filter(receipts.Description.like(f'%{formData["Description"]}%'))\
			# .order_by(receipts.ReceiptID):

		returnSet['data'] += [{'ReceiptID': r.ReceiptID, 'Description': r.Description, 'Amount': float(r.Amount), 'Username': r.Username, 'PurchaseDate': r.PurchaseDate}]
		# print(r,u)
	


	return returnSet

def receipts_receipt(ReceiptID):
	engine = create_engine('mysql+pymysql://'+config.DATABASE_USERNAME+':'+config.DATABASE_PASSWORD+'@'+config.DATABASE_HOSTNAME+'/'+config.DATABASE_NAME, echo=True)

	Session = sessionmaker(bind=engine)
	session = Session()

	receipts = Table('Receipts', meta, autoload=True, autoload_with=engine)
	receiptsUsers = Table('ReceiptsUsers', meta, autoload=True, autoload_with=engine)
	Users = Table('Users', meta, autoload=True, autoload_with=engine)

	j = join(Receipts, ReceiptsUsers, Receipts.ReceiptID == ReceiptsUsers.ReceiptID)
	qry = session.query(j)

	returnSet = {'receipt': []}
	for i in qry.filter(Receipts.ReceiptID == ReceiptID):
		returnSet['receipt'] += [{'ReceiptID': i.ReceiptID, 'Description': i.Description, 'Amount': i.Amount}]




	return returnSet


