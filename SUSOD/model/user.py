"""
Handles login/logout/create/delete requests.
"""
import flask
import SUSOD
from SUSOD.util import *

from SUSOD.model.db import get_db

# TODO need better returns and logic in case of failure

def model_user_login(username, password):
	"""
	verifies user login
	"""
	cursor = get_db().cursor()

	#https://www.w3schools.com/python/python_mysql_insert.asp
	sql = """
		SELECT * FROM Users U
		WHERE U.username = (%s)
		"""

	cursor.execute(sql, (username,))

	# unique index on username, if this returns more than 1...
	user_info = cursor.fetchone()
	
	# TODO use dict cursors so we can get col names
	if (password_db_string_verify(password, user_info[2])):
		login_user(username)
	else:
		return None
	



def model_user_create(username, password1, password2):
	"""
	creates user in db
	"""
	if password1 != password2:
		# TODO throw exception
		return None

	cursor = get_db().cursor()
	sql = """
		INSERT INTO Users (Username, Password)
		VALUES (%s, %s)
		"""

	password = password_db_string_create(password1)
	try:
		cursor.execute(sql, (username, password))
	except:
		return None

	login_user(username)
	return