"""
Handles login/logout/create/delete requests.
"""
import flask
import SUSOD
import SUSOD.util

from SUSOD.model.db import get_db

# TODO need better returns and logic in case of failure

def model_user_login(username, password):
	"""
	verifies user login
	"""
	cursor = get_db().cursor(dictionary=True)

	#https://www.w3schools.com/python/python_mysql_insert.asp
	sql = """
		SELECT U.Password FROM Users U
		WHERE U.Username = (%s)
		"""

	cursor.execute(sql, (username,))

	# unique index on username, if this returns more than 1...
	user_info = cursor.fetchone()
	
	if (SUSOD.util.password_db_string_verify(password, user_info['Password'])):
		SUSOD.util.login_user(username)
		return
	else:
		raise Exception('unable to login as user: \'{}\''.format(username))
	



def model_user_create(username, password1, password2):
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

	password = SUSOD.util.password_db_string_create(password1)
	try:
		cursor.execute(sql, (username, password, None, None, 'TestLastName'))
	except:
		raise
		#raise Exception('unable to create user: \'{}\''.format(username))

	SUSOD.util.login_user(username)
	return