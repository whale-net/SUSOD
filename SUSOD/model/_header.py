"""
Handles api requests for the header
"""

import flask
import SUSOD
import SUSOD.util

from SUSOD.model.db import get_db

def model_get_menu_options():
	"""
	returns list of menu options
	"""
	cursor = get_db().cursor(dictionary=True)

	sql = """
		SELECT MO.MenuText, MO.MenuLink, MO.Order, MO.MenuOptionID
		FROM MenuOptions MO
		WHERE MO.IsVisible = 1
		ORDER BY MO.Order ASC
		"""

	cursor.execute(sql)

	return cursor.fetchall()
