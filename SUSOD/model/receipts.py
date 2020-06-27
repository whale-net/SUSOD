import flask
import SUSOD
import datetime
from SUSOD import util
from SUSOD import config

from .db import *
from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, MetaData, Table, join, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists, text


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

def receipts_save(formData):
	engine = create_engine('mysql+pymysql://'+config.DATABASE_USERNAME+':'+config.DATABASE_PASSWORD+'@'+config.DATABASE_HOSTNAME+'/'+config.DATABASE_NAME, echo=True)
	# Session = sessionmaker(bind=engine)

	# session = Session()
	
	# meta = MetaData()
	
	# receipts = Table('Receipts', meta, autoload=True, autoload_with=engine)
	# users = Table('Users', meta, autoload=True, autoload_with=engine)	
	ReceiptID = 0
	CreatedUpdatedAt = datetime.datetime.now()
	 
	if (formData['receipt']["ReceiptID"] > 0):
		with engine.connect() as con:

			sql = text(
				"""
				UPDATE Receipts
				SET Description = :Description 
					, OwnerUserID = :OwnerUserID
					, Amount = :Amount
					, PurchaseDate = :PurchaseDate
				WHERE ReceiptID = :ReceiptID

				"""
				)

			data = {"ReceiptID": formData['receipt']["ReceiptID"], "Description": formData['receipt']["Description"], "OwnerUserID": formData['receipt']["OwnerUserID"], "Amount": formData['receipt']['Amount'], "PurchaseDate":  datetime.datetime.strptime( formData["receipt"]['PurchaseDate'], '%Y-%m-%dT%H:%M:%S.%fZ')}
			#TODO: Look into sqlalchemy.engine.result.ResultProxy....
			print(con.execute(sql, **data))

			ReceiptID = formData['receipt']['ReceiptID']
	else:
		with engine.connect() as con:

			sql = text(
				"""
				INSERT into Receipts (OwnerUserID , Amount , PurchaseDate , CreatedBy , CreatedDate , UpdatedBy , UpdatedDate, Description, ReceiptTypeID )
				Values (:OwnerUserID , :Amount , :PurchaseDate , :CreatedBy , :CreatedDate , :UpdatedBy , :UpdatedDate, :Description, :ReceiptTypeID );

				SELECT LAST_INSERT_ID() ReceiptID
				"""
				)

			#required keys
			data = {"OwnerUserID": formData['receipt']["OwnerUserID"], "Amount": formData['receipt']['Amount'], "CreatedBy": formData['UserID'], "UpdatedBy": formData['UserID'], "PurchaseDate": datetime.datetime.strptime( formData["receipt"]['PurchaseDate'], '%Y-%m-%dT%H:%M:%S.%fZ'),
					"CreatedDate": CreatedUpdatedAt, "UpdatedDate": CreatedUpdatedAt, "Description": formData['receipt']['Description'],
					"ReceiptTypeID": 1 #todo add receipt types
					}	

			# can add optional as (if thing in formData[...]: add to data, else add None in place). no optional for this page
			for i in con.execute(sql, **data):
				ReceiptID = i.ReceiptID

	print(formData['receiptsUsers']);

	#first delete existing ReceiptsUsers records 
	with engine.connect() as con:

		sql = text(
			"""
			DELETE 
			FROM ReceiptsUsers 
			WHERE ReceiptID = :ReceiptID
			"""
			)

		#required keys
		data = {"ReceiptID": ReceiptID}
		con.execute(sql, **data)
		


	if (len(formData['receiptsUsers']) > 0 ):
		
		for i in formData['receiptsUsers']:
			#add individually
			with engine.connect() as con:

				sql = text(
					"""
					INSERT into ReceiptsUsers (ReceiptID , UserID, PaymentRatio, DeductionAmount , CreatedBy, CreatedDate , UpdatedBy , UpdatedDate )
					values (:ReceiptID , :UserID, :PaymentRatio, :DeductionAmount , :CreatedBy, :CreatedDate , :UpdatedBy , :UpdatedDate )

					"""
					)

				#required keys
				data = {"ReceiptID": ReceiptID, "UserID": i['UserID'], "PaymentRatio": i["PaymentRatio"], "DeductionAmount": i["DeductionAmount"], "CreatedBy": formData['UserID'],
						"UpdatedBy": formData['UserID'], "CreatedDate": CreatedUpdatedAt, "UpdatedDate": CreatedUpdatedAt	}
				con.execute(sql, **data)
	 
	
		
	return formData

def receipts_setup():
	engine = create_engine('mysql+pymysql://'+config.DATABASE_USERNAME+':'+config.DATABASE_PASSWORD+'@'+config.DATABASE_HOSTNAME+'/'+config.DATABASE_NAME, echo=True)
	Session = sessionmaker(bind=engine)

	session = Session()
	
	meta = MetaData()
	#meta.reflect(bind=engine)

	receipts = Table('Receipts', meta, autoload=True, autoload_with=engine)
	users = Table('Users', meta, autoload=True, autoload_with=engine)
	
	returnSet = {'data': []}
	for r in session.query(receipts, users)\
			.join( receipts, receipts.c['OwnerUserID'] == users.c["UserID"])\
			.order_by(receipts.c['ReceiptID']):
		returnSet['data'] += [{'ReceiptID': r.ReceiptID, 'Description': r.Description, 'Amount': float(r.Amount), 'Username': r.Username, 'PurchaseDate': r.PurchaseDate}]



	return returnSet


def receipts_search(formData):
	engine = create_engine('mysql+pymysql://'+config.DATABASE_USERNAME+':'+config.DATABASE_PASSWORD+'@'+config.DATABASE_HOSTNAME+'/'+config.DATABASE_NAME, echo=True)

	Session = sessionmaker(bind=engine)
	session = Session()
	

	meta = MetaData()
	#meta.reflect(bind=engine)

	receipts = Table('Receipts', meta, autoload=True, autoload_with=engine)
	users = Table('Users', meta, autoload=True, autoload_with=engine)
	#receipts = meta.tables["Receipts"]
	#users = meta.tables["Users"]
	receiptsUsers = Table('ReceiptsUsers', meta, autoload=True, autoload_with=engine)

	returnSet = {'data': []}
	
	if formData["OnlyShowUnpaid"] == False:
		#sqlalchemy PyObject manipulation (perhaps better when doing in memory?)
		for r in session\
				.query(receipts, users)\
				.join( receipts, receipts.c['OwnerUserID'] == users.c["UserID"])\
				.filter(receipts.c['Description'].like(f'%{formData["Description"]}%'))\
				.order_by(receipts.c['ReceiptID']):
				# .query(receipts, users)\
				# .join(users, receipts.OwnerUserID == users.UserID)\
				# .order_by(receipts.ReceiptID):

			returnSet['data'] += [{'ReceiptID': r.ReceiptID, 'Description': r.Description, 'Amount': float(r.Amount), 'Username': r.Username, 'PurchaseDate': r.PurchaseDate}]
			# print(r,u)
	else:
		#sqlalchemy text 
		with engine.connect() as con:

			sql = text(
				"""
				SELECT R.ReceiptID, R.Description, R.Amount, U.Username, R.PurchaseDate
				FROM Receipts R
				inner join Users U on R.OwnerUserID = U.UserID 

				WHERE NOT EXISTS
					(select *
						from PaymentsReceipts PR2 
						where PR2.ReceiptID = R.ReceiptID 
					)

				AND R.Description LIKE :Description

				ORDER BY R.ReceiptID

				"""
				)

			data = {"Description": f'%{formData["Description"]}%' }

			for r in con.execute(sql, **data):
		
				returnSet['data'] += [{'ReceiptID': r.ReceiptID, 'Description': r.Description, 'Amount': float(r.Amount), 'Username': r.Username, 'PurchaseDate': r.PurchaseDate}]
		

	return returnSet

def receipts_receipt(ReceiptID):
	engine = create_engine('mysql+pymysql://'+config.DATABASE_USERNAME+':'+config.DATABASE_PASSWORD+'@'+config.DATABASE_HOSTNAME+'/'+config.DATABASE_NAME, echo=True)

	Session = sessionmaker(bind=engine)
	session = Session()

	# meta = MetaData()
	# meta.reflect(bind=engine)


	# receipts = Table('Receipts', meta, autoload=True, autoload_with=engine)
	# receiptsUsers = Table('ReceiptsUsers', meta, autoload=True, autoload_with=engine)

	# j = join(receipts, receiptsUsers, receipts.c['ReceiptID'] == receiptsUsers.c['ReceiptID'])
	# qry = session.query(j)

	# users = Table('Users', meta, autoload=True, autoload_with=engine)

	returnSet = {'receipt': [], 'users': [], 'receiptsUsers': []}
	# for i in qry.filter(receipts.c['ReceiptID'] == ReceiptID):
	# 	returnSet['receipt'] += [{'ReceiptID': i.ReceiptID, 'Description': i.Description, 'Amount': float(i.Amount), 'OwnerUserID': i.OwnerUserID}]
	if (ReceiptID != 0):
		with engine.connect() as con:
			sql = text(
				"""
				SELECT *
				FROM Receipts R 
				WHERE R.ReceiptID = :ReceiptID
				"""
				)
			data = {"ReceiptID": ReceiptID }
			for r in con.execute(sql, **data):
				print(r)
				returnSet['receipt'] += [{'ReceiptID': r.ReceiptID, 'Description': r.Description, 'Amount': float(r.Amount), 'OwnerUserID': r.OwnerUserID, 'PurchaseDate': r.PurchaseDate}]


		with engine.connect() as con:

			sql = text(
				"""
				SELECT ru.UserID , IFNULL(ru.DeductionAmount, 0) DeductionAmount , ru.PaymentRatio 
				from ReceiptsUsers ru 
				where ru.ReceiptID = :ReceiptID 
				and ru.Deleted = 0
				"""
			)
			data = {"ReceiptID": ReceiptID }

			for r in con.execute(sql, **data):
				returnSet['receiptsUsers'] += [{'UserID': r.UserID, 'DeductionAmount': float(r.DeductionAmount), 'PaymentRatio': r.PaymentRatio}]
	else: 
		returnSet['receipt'] += [{'ReceiptID': 0, 'PurchaseDate': datetime.datetime.now() }]

	with engine.connect() as con:
		print("USERS")
		sql = text(
			"""
			SELECT UserID, Username
			from Users
			where FirstName IS NOT NULL  
			"""
			)

		#initial 
		returnSet['users'] += [{'UserID': -1, 'Username': '--Select--'}]

		for i in con.execute(sql):
			returnSet['users'] += [{'UserID': i.UserID, 'Username': i.Username}]


	return returnSet


