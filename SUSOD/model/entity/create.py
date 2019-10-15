import math
import datetime

import flask
from werkzeug.utils import secure_filename

import SUSOD
from SUSOD import model
from SUSOD import util


from ..db import *


class Entity:

	MAX_FILE_PART_SIZE = 16777216 - 1 # 16 MB / MEDIUMBLOB -> needs to be 1 byte less else sql connector goes dead

	def __init__(self):
		self.EntityID = None
		self.Description = None
		self.EntityTypeID = None
		self.Filename = None

		self._file_bytes = None 

	# unsure if we should have a constructor to create a file automatically, seems like it could cause problems

	def get_file_size(self):
		return self.file_size

	def create(self, file, file_name=None):
		"""
		Take a file
		"""
		if file == None:
			raise ValueError("file is not valid")
		self._file = file

		if file_name == None:
			try:
				file_name = self._file.filename
			except:
				file_name = None
		file_name = secure_filename(file_name)
		self.Filename = file_name

		if self.EntityID != None:
			raise RuntimeError("Entity - Entity already exists")

		# surely there has to be a better way to do this
		self.file_extension = self.Filename.split('.')[-1]
		if len(self.file_extension) > 5: # probably not an extension, made up number, can change or remove
			self.file_extension = None


		# break up file
		self.__file_bytes = self._file.read()
		# write first to get entity ID
		first_entity_part = EntityPart(self.__file_bytes[0:Entity.MAX_FILE_PART_SIZE], EntityPart.INSERT_ORDER_BEGIN)
		first_entity_part.write_to_db()
		self.EntityID = first_entity_part.get_EntityID()
		self._entity_parts = [first_entity_part]
		self.file_size = len(self.__file_bytes)
		for file_part_idx in range(1, math.ceil(1.0 * self.get_file_size() / Entity.MAX_FILE_PART_SIZE)):
			entity_part_bytes = self.__file_bytes[(file_part_idx * Entity.MAX_FILE_PART_SIZE):((file_part_idx + 1) * Entity.MAX_FILE_PART_SIZE)]
			self._entity_parts.append(EntityPart(entity_part_bytes, file_part_idx + EntityPart.INSERT_ORDER_BEGIN, EntityID=self.EntityID))
			
		# Begin writing to DB
		insert_start = datetime.datetime.now()
		for entity_part in self._entity_parts:
			entity_part.write_to_db()
		
		print(f"""
Entity [{int(self.EntityID)}] inserted in: {(datetime.datetime.now() - insert_start)} 
	Bytes: {self.file_size}
	Parts: {len(self._entity_parts)}
""")

		# todo handle deleting of entity on fail





class EntityPart:

	# In case we ever want to prepend files?
	INSERT_ORDER_BEGIN = 1

	def __init__(self, FilePart, InsertOrder, EntityID=None, EntityPartID=None):
		self.EntityPartID = EntityPartID
		self.EntityID = EntityID
		self.InsertOrder = InsertOrder
		self.FilePart = FilePart

		if self.EntityID == None and self.InsertOrder == EntityPart.INSERT_ORDER_BEGIN:
			self.NewEntity = True
		else:
			self.NewEntity = False

		self._cursor = None

	# todo with defaults
	# def __init__(self, EntityPartID, InsertOrder, FilePart):
	# 	self.EntityPartID = EntityPartID
	# 	self.InsertOrder = InsertOrder
	# 	self.FilePart = FilePart

	def write_to_db(self, FileName=None, file_extension=None):
		if self.EntityPartID != None:
			return (self.EntityID, self.EntityPartID)
		try:
			# setup cursor as needed, not initially so we don't get too many connections
			self._cursor = get_db(raw=True).cursor()
			if self.NewEntity:
				self._new_entity(FileName, file_extension)
			else:
				self._append_entity()
		except Exception as e:
			print(e)
			self._delete_from_db()
			


	def _delete_from_db(self):
		# don't delete Entity here because of foreign keys
		self._cursor.execute("""DELETE FROM EntityParts WHERE EntityPartID = (%s)""", (self.EntityPartID,))
		self._cursor.close()

	def _new_entity(self, FileName, file_extension):
		print(f'New Entity Being Created @ [{str(datetime.datetime.now())}]')

		args = (self.get_FilePart_db(), FileName, file_extension, util.get_UserID(), None, None) # None is for outEntityID, outEntityPartID
		self._sql_results = self._cursor.callproc('spCreateEntity', args)
		self.EntityID = int(self._sql_results[4])
		self.EntityPartID = int(self._sql_results[5])

		if self.EntityID == None:
			raise RuntimeError("uh oh, something went fucko when creating the entity")
		if self.EntityPartID == None:
			raise RuntimeError("uh oh, something went fucko when creating the entitypart")

		print(f'Entity [{self.EntityID}] was created @ [{str(datetime.datetime.now())}]')

	def _append_entity(self):
		print(f'Entity [{self.EntityID}] writing Part [{self.InsertOrder}] @ [{str(datetime.datetime.now())}]')

		args = (self.EntityID, self.get_FilePart_db(), self.InsertOrder, None)
		self._sql_results = self._cursor.callproc('spAppendEntity', args)
		self.EntityPartID = int(self._sql_results[3])

		if self.EntityPartID == None:
			raise RuntimeError("uh oh, something went fucko when creating the entity")


	def set_EntityPartID(self, EntityPartID):
		self.EntityPartID = EntityPartID

	def get_EntityPartID(self):
		return self.EntityPartID

	def get_EntityID(self):
		return self.EntityID

	def get_FilePart_db(self):
		# in case we ever need to switch out of raw connections, we can format as b64 or hex
		return self.FilePart

	def get_InsertOrder(self):
		return self.InsertOrder
