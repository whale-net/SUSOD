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
	 
	print(formData)

	if (formData['receipt']["ReceiptID"] > 0):
		with engine.connect() as con:

			sql = text(
				"""
				UPDATE Receipts
				SET Description = :Description 
					, OwnerUserID = :OwnerUserID
					, Amount = :Amount
					, PurchaseDate = :PurchaseDate
					, UpdatedBy = :UpdatedBy
					, UpdatedDate = :UpdatedDate
				WHERE ReceiptID = :ReceiptID 
				"""
				)

			data = {"ReceiptID": formData['receipt']["ReceiptID"], "Description": formData['receipt']["Description"], "OwnerUserID": formData['receipt']["OwnerUserID"], "Amount": formData['receipt']['Amount']
					, "PurchaseDate":  datetime.datetime.strptime( formData["receipt"]['PurchaseDate'], '%Y-%m-%dT%H:%M:%S.%fZ')
					, "UpdatedDate": CreatedUpdatedAt, "UpdatedBy": formData['UserID'] }
			#TODO: Look into sqlalchemy.engine.result.ResultProxy....
			print(con.execute(sql, **data))

			ReceiptID = formData['receipt']['ReceiptID']
	else:
		with engine.connect() as con:

			sql = text(
				"""
				INSERT into Receipts (OwnerUserID , Amount , PurchaseDate , CreatedBy , CreatedDate , UpdatedBy , UpdatedDate, Description, ReceiptTypeID )
				Values (:OwnerUserID , :Amount , :PurchaseDate , :CreatedBy , :CreatedDate , :UpdatedBy , :UpdatedDate, :Description, :ReceiptTypeID );

				"""
				)

			#required keys
			data = {"OwnerUserID": formData['receipt']["OwnerUserID"], "Amount": formData['receipt']['Amount'], "CreatedBy": formData['UserID'], "UpdatedBy": formData['UserID'], "PurchaseDate": datetime.datetime.strptime( formData["receipt"]['PurchaseDate'], '%Y-%m-%dT%H:%M:%S.%fZ'),
					"CreatedDate": CreatedUpdatedAt, "UpdatedDate": CreatedUpdatedAt, "Description": formData['receipt']['Description'],
					"ReceiptTypeID": 1 #todo add receipt types
					}	

			# can add optional as (if thing in formData[...]: add to data, else add None in place). no optional for this page
			con.execute(sql, **data)
				# ReceiptID = iReceiptID


			sql = text(
				"""
				SELECT LAST_INSERT_ID() ReceiptID
				"""
				)
			for i in con.execute(sql):
				ReceiptID = i.ReceiptID
				formData['receipt']['ReceiptID'] = ReceiptID



	# #first delete existing ReceiptsUsers records 
	# with engine.connect() as con:

	# 	sql = text(
	# 		"""
	# 		DELETE 
	# 		FROM ReceiptsUsers 
	# 		WHERE ReceiptID = :ReceiptID
	# 		"""
	# 		)

	# 	#required keys
	# 	data = {"ReceiptID": ReceiptID}
	# 	con.execute(sql, **data)

		

	if (len(formData['receiptsUsers']) > 0 ):
		
		for i in formData['receiptsUsers']:
			#add individually
			with engine.connect() as con:

				receiptUser = formData['receiptsUsers'][i][0]
				print(receiptUser)
				if receiptUser['ReceiptUserID'] > 0:
					sql = text(
					"""
					UPDATE ReceiptsUsers
					SET PaymentRatio = :PaymentRatio,
						DeductionAmount = :DeductionAmount,
						UpdatedBy = :UpdatedBy,
						UpdatedDate = :UpdatedDate,
						Deleted = :Deleted
					WHERE ReceiptUserID = :ReceiptUserID

					"""
					)

					data = {"ReceiptUserID": receiptUser['ReceiptUserID'], "PaymentRatio": receiptUser["PaymentRatio"], "DeductionAmount": receiptUser["DeductionAmount"], 
							"UpdatedBy": i, "UpdatedDate": CreatedUpdatedAt, "Deleted": receiptUser["Deleted"]	}
					con.execute(sql, **data)

				else:
					sql = text(
					"""
					INSERT into ReceiptsUsers (ReceiptID , UserID, PaymentRatio, DeductionAmount , CreatedBy, CreatedDate , UpdatedBy , UpdatedDate, Deleted )
					values (:ReceiptID , :UserID, :PaymentRatio, :DeductionAmount , :CreatedBy, :CreatedDate , :UpdatedBy , :UpdatedDate, :Deleted)

					"""
					)

					#required keys
					data = {"ReceiptID": ReceiptID, "UserID": i, "PaymentRatio": receiptUser["PaymentRatio"], "DeductionAmount": receiptUser["DeductionAmount"], "CreatedBy": formData['UserID'],
							"UpdatedBy": formData['UserID'], "CreatedDate": CreatedUpdatedAt, "UpdatedDate": CreatedUpdatedAt, "Deleted": receiptUser["Deleted"]	}
					con.execute(sql, **data)

				

	# Run a search so we get up to date!!
	return receipts_receipt(ReceiptID)

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
	
		#sqlalchemy PyObject manipulation (perhaps better when doing in memory?)
		# for r in session\
		# 		.query(receipts, users)\
		# 		.join( receipts, receipts.c['OwnerUserID'] == users.c["UserID"])\
		# 		.filter(receipts.c['Description'].like(f'%{formData["Description"]}%'))\
		# 		.order_by(receipts.c['ReceiptID']):
				

			# returnSet['data'] += [{'ReceiptID': r.ReceiptID, 'Description': r.Description, 'Amount': float(r.Amount), 'Username': r.Username, 'PurchaseDate': r.PurchaseDate}]
			# print(r,u)

		#sqlalchemy text 
	with engine.connect() as con:
		

		data = {"Description": f'%{formData["Description"] if (formData["Description"] != None) else ""}%'}

		sql = """
SELECT R.ReceiptID, R.Description, R.Amount, U.Username, R.PurchaseDate
FROM Receipts R
inner join Users U on R.OwnerUserID = U.UserID 



WHERE R.Description LIKE :Description

		"""
	
		if (formData["Amount"] != None and formData["Amount"] != ''):
			sql += """ 
AND R.Amount = :Amount 
			"""
			
			data["Amount"] = formData["Amount"]

		if formData["OnlyShowUnpaid"] == True:
			sql += """ 			
AND NOT EXISTS
	(select *
		from PaymentsReceipts PR2 
		where PR2.ReceiptID = R.ReceiptID 
	)
			"""


		sql += """

ORDER BY R.ReceiptID

				"""


		for r in con.execute(text(sql), **data):
	
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

	returnSet = {'receipt': {}, 'users': [], 'receiptsUsers': []}
	# for i in qry.filter(receipts.c['ReceiptID'] == ReceiptID):
	# 	returnSet['receipt'] += [{'ReceiptID': iReceiptID, 'Description': i.Description, 'Amount': float(i.Amount), 'OwnerUserID': i.OwnerUserID}]
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
				returnSet['receipt'] = {'ReceiptID': r.ReceiptID, 'Description': r.Description, 'Amount': float(r.Amount), 'OwnerUserID': r.OwnerUserID, 'PurchaseDate': r.PurchaseDate}

		if (returnSet['receipt'] == {}):
			returnSet['receipt']['PurchaseDate'] = datetime.datetime.now()


		with engine.connect() as con:

			sql = text(
				"""
				SELECT ru.*
				from ReceiptsUsers ru 
				where ru.ReceiptID = :ReceiptID 
				
				"""
			)
			data = {"ReceiptID": ReceiptID }

			returnSet['receiptsUsers'] = {}
			for ru in con.execute(sql, **data):
				 #[{'UserID': r.UserID, 'DeductionAmount': float(r.DeductionAmount), 'PaymentRatio': r.PaymentRatio}]
				returnSet['receiptsUsers'][ru.UserID] = [{'ReceiptUserID': ru.ReceiptUserID, 'ReceiptID': ru.ReceiptID, 'UserID': ru.UserID, 
					'CreatedBy': ru.CreatedBy, 'CreatedDate': ru.CreatedDate, 'UpdatedBy': ru.UpdatedBy, 'UpdatedDate': ru.UpdatedDate}]

				if ru.Deleted == b'\x00':
					returnSet['receiptsUsers'][ru.UserID][0]['Deleted'] = False
				else: 
					returnSet['receiptsUsers'][ru.UserID][0]['Deleted'] = True


				if ru.PaymentRatio != None:
					returnSet['receiptsUsers'][ru.UserID][0]['PaymentRatio'] = float(ru.PaymentRatio)
				if ru.DeductionAmount != None:
					returnSet['receiptsUsers'][ru.UserID][0]['DeductionAmount'] = float(ru.DeductionAmount)
					
	else: 
		returnSet['receipt'] = {'ReceiptID': 0, 'PurchaseDate': datetime.datetime.now(), 'Amount': '', 'OwnerUserID': 0, 'Description': ''  } #default params...
		returnSet['receiptsUsers'] = {} # reset receipts users

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
		returnSet['userSet'] = {}

		for i in con.execute(sql):
			returnSet['users'] += [{'UserID': i.UserID, 'Username': i.Username}]
			returnSet['userSet'][i.UserID] = i.Username

	returnSet['ReceiptID'] = ReceiptID

	return returnSet

