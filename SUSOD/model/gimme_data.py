"""
Example script to query from test table.

Makes sure that we can have our model setup like this.
"""
import flask
import SUSOD

from SUSOD.model.db import get_db


def get_test_data():
	"""
	Return test data from database.
	"""
	cursor = get_db().cursor();

	cursor.execute(
		"""
		SELECT * FROM test
		"""
	)

	return cursor.fetchall()	


def giveme_data(information):
	"""
	Inserts data into test table.
	"""
	cursor = get_db().cursor();

	#https://www.w3schools.com/python/python_mysql_insert.asp
	sql = """
		INSERT INTO test(information)
		VALUES (%s)
		"""

	cursor.execute(
		sql,
		# NOTE: single value inserts must be formatted like this
		(information,)
	)