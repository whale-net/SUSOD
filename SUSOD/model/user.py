"""
Handles login/logout/create/delete requests.
"""
import flask
import SUSOD
#import SUSOD.util
from SUSOD import util

from .db import *

# TODO need better returns and logic in case of failure

def user_login(username, password):
	"""
	verifies user login
	"""
	cursor = get_db().cursor(dictionary=True)

	#https://www.w3schools.com/python/python_mysql_insert.asp
	sql = """
		SELECT U.Password, U.UserID, U.Username
		FROM Users U
		WHERE U.Username = (%s)
		"""

	cursor.execute(sql, (username,))

	# unique index on username, if this returns more than 1...
	user_info = cursor.fetchone()
	print('ok1')
	
	if (util.password_db_string_verify(password, user_info['Password'])):
		util.login_user(user_info['UserID'], user_info['Username'])
		print('ok2')
		return
	else:
		raise Exception('unable to login as user: \'{}\''.format(username))
	



def user_create(username, password1, password2):
	"""
	creates user in db
	"""
	if password1 != password2:
		raise Exception('passwords not equal')

	cursor = get_db().cursor()
	sql = """
		INSERT INTO Users (Username, Password, FirstName, MiddleName, LastName)
		VALUES (%s, %s, %s, %s, %s)
		"""

	password = util.password_db_string_create(password1)
	try:
		cursor.execute(sql, (username, password, None, None, 'TestLastName'))
	except:
		raise
		#raise Exception('unable to create user: \'{}\''.format(username))

	SUSOD.util.login_user(username)
	return


def user_index_setup(UserID):
	"""
	returns information for user index page.
	"""
	cursor = get_db().cursor(dictionary=True)
	sql = """
		SELECT U.Username, U.FirstName, U.MiddleName, U.LastName
			, U.BirthDate, U.AvatarEntityID
		FROM Users U
		WHERE U.UserID = :UserID
		"""
	try:
		db = db_connection()
		data = db.query(sql, UserID=UserID)
		return next(data)
	except:
		raise

def user_index_update(UserID, user_info):
	"""
	updates user information with information from page
	"""

	try:
		# cursor.execute(sql, (user_info['FirstName'], user_info['LastName'], UserID))
		db = db_connection()
		update_dict = dict(
			UserID = UserID,
			FirstName = user_info['FirstName'],
			LastName = user_info['LastName']
		)

		db['Users'].update(update_dict, ['UserID'])
		return user_index_setup(UserID)
	except:
		raise


def user_update_avatar(UserID, EntityID):
	"""
	verifies user login, returns the id
	"""
	cursor = get_db().cursor()

	sql = """
		UPDATE Users SET AvatarEntityID = (%s) WHERE UserID = (%s)
		"""

	cursor.execute(sql, (EntityID, UserID,))


def user_login_return_id(username, password):
	"""
	verifies user login, returns the id
	"""
	cursor = get_db().cursor(dictionary=True)

	#https://www.w3schools.com/python/python_mysql_insert.asp
	sql = """
		SELECT U.Password, U.UserID, U.Username
		FROM Users U
		WHERE U.Username = (%s)
		"""

	cursor.execute(sql, (username,))

	# unique index on username, if this returns more than 1...
	user_info = cursor.fetchone()
	print('ok1')
	
	if (util.password_db_string_verify(password, user_info['Password'])):
		util.login_user(user_info['UserID'], user_info['Username'])
		print('ok2')
		return user_info['UserID']
	else:
		raise Exception('unable to login as user: \'{}\''.format(username))
	
	return -1