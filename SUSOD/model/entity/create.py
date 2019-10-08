



import flask
import SUSOD
from SUSOD import model
from werkzeug.utils import secure_filename
from ..db import *




def insert_file(file, file_name=None):

	if file_name == None:
		try:
			file_name = file.filename
		except:
			# just set to unknown
			file_name = None

	file_name = secure_filename(file_name)
	extension = file_name.split('.')[-1]



	if len(extension) > 5: # probably not an extension, it ain't perfect
		extension = None

	print(file_name, extension)
	_modify_entity(file)

	return 


def _modify_entity(file_part, EntityID=None):
	cursor = get_db().cursor()

	cursor.callproc()


