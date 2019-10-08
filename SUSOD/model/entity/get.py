"""
Get Datafiles.
"""
#from ..model import db

from ..db import *

def get_file(EntityID):
	"""
	Returns a complete file
	"""
	sql = """
		SELECT * FROM Users
		"""

	db = db_connection()
	