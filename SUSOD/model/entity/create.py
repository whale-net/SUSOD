import binascii

import flask
from werkzeug.utils import secure_filename

import SUSOD
from SUSOD import model
from SUSOD import util


from ..db import *



def insert_file(file, file_name=None):

	if file_name == None:
		try:
			file_name = file.filename
		except:
			# just set to unknown
			file_name = None

	file_name = secure_filename(file_name)
	# surely there has to be a better way to do this
	file_extension = file_name.split('.')[-1]



	if len(file_extension) > 5: # probably not an extension, it ain't perfect
		file_extension = None

	print('before')

	# print(file.read())
	file_part = file.read()
	file_part = binascii.hexlify(file_part)
	print(type(file_part))
	# _create_entity(file.read(), file_name, file_extension)
	_create_entity(file_part, file_name, file_extension)

	return 


def _create_entity(filepart, file_name, file_extension):
	cursor = get_db().cursor()

	EntityID = -1

	args = (filepart, file_name, file_extension, util.get_UserID(), 0)
	cursor.callproc('spCreateEntity', args)
	#get_db().commit()
	print('value', EntityID, args[4])
	return EntityID





