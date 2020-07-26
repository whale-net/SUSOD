import flask
import SUSOD

from SUSOD import util
from .db import get_db
from SUSOD import config

from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, MetaData, Table, join, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists, text

def transactions_search(IsShowAll):
	engine = create_engine('mysql+pymysql://'+config.DATABASE_USERNAME+':'+config.DATABASE_PASSWORD+'@'+config.DATABASE_HOSTNAME+'/'+config.DATABASE_NAME, echo=True)


	returnSet = {'transactions': []};
	
	with engine.connect() as con:
		sql = """
SELECT us.Username Sender, ur.Username  Receiver, TransactionAmount , t.TransactionID , IsReceiverConfirmed , IsSenderConfirmed , SenderUserID, ReceiverUserID
FROM Transactions t 
inner join Users  us on t.SenderUserID =us.UserID 
inner join Users  ur on t.ReceiverUserID =ur.UserID 
			"""
			

		if not IsShowAll:
			sql += """
	WHERE (t.IsSenderConfirmed  = 0 or t.IsReceiverConfirmed  = 0)
	"""

		# sql parms go here as {"ParmName": ParmValue, ... }
		data = {}
		
		for r in con.execute(text(sql), **data):
			print(r)
			returnSet['transactions'] += [{'Sender': r.Sender, 'Receiver': r.Receiver, 'TransactionAmount': float(r.TransactionAmount)
				, 'TransactionID': r.TransactionID, 'SenderUserID': r.SenderUserID, 'ReceiverUserID': r.ReceiverUserID
				, 'IsReceiverConfirmed': int.from_bytes(r.IsReceiverConfirmed,  byteorder='big'), 'IsSenderConfirmed': int.from_bytes(r.IsSenderConfirmed,  byteorder='big')}]


	


	return returnSet


def transactions_confirm(SenderReceiver, TransactionID):
	engine = create_engine('mysql+pymysql://'+config.DATABASE_USERNAME+':'+config.DATABASE_PASSWORD+'@'+config.DATABASE_HOSTNAME+'/'+config.DATABASE_NAME, echo=True)


	returnSet = {'transactions': []};
	
	with engine.connect() as con:
		if (SenderReceiver == 'receiver'):
			sql = """
UPDATE Transactions
SET IsReceiverConfirmed=1
WHERE TransactionID=:TransactionID;

				"""
		else:
			sql = """
UPDATE Transactions
SET IsSenderConfirmed=1
WHERE TransactionID=:TransactionID;

				"""

		

		# sql parms go here as {"ParmName": ParmValue, ... }
		data = {"TransactionID": TransactionID}
		
		con.execute(text(sql), **data)
			
			

	return returnSet
