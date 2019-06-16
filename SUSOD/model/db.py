"""
MySQL database connection manager.

Creates database connection to be used.
"""
import flask
import SUSOD
import mysql.connector


def get_db():
	""" Return (or create/return) a mysql connection."""
	if not hasattr(flask.g, 'db'):
		flask.g.db = mysql.connector.connect(
			host=SUSOD.app.config['DATABASE_HOSTNAME'],
			user=SUSOD.app.config['DATABASE_USERNAME'],
			passwd=SUSOD.app.config['DATABASE_PASSWORD'],
			database=SUSOD.app.config['DATABASE_NAME']
		)

	return flask.g.db


@SUSOD.app.teardown_appcontext
def close_db(error):
	"""Close database at the end of a request."""
	if hasattr(flask.g, 'db'):
		flask.g.db.commit()
		flask.g.db.close()