import binascii
import math

import flask
from werkzeug.utils import secure_filename

import SUSOD
from SUSOD import model
from SUSOD import util


from ..db import *


class Entity:

	MAX_FILE_PART_SIZE = 16777216 # 16 MB / MEDIUMBLOB

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
		print(type(self._file))

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
		self.file_size = len(self.__file_bytes)
		self._entity_parts = []	
		for file_part_idx in range(0, math.ceil(1.0 * self.get_file_size() / Entity.MAX_FILE_PART_SIZE)):
			entity_part_bytes = self.__file_bytes[(file_part_idx * Entity.MAX_FILE_PART_SIZE):((file_part_idx + 1) * Entity.MAX_FILE_PART_SIZE)]
			entity_part = EntityPart(entity_part_bytes, file_part_idx)
			self._entity_parts.append(entity_part)
			
		# Begin writing to DB
		print(self._entity_parts)
		for entity_part in self._entity_parts:
			if self.EntityID == None:
				self._new_entity(entity_part)
			else:
				self._append_entity(entity_part)
				continue

	def _new_entity(self, entity_part):
		cursor = get_db().cursor()
		args = (entity_part.get_FilePart_db(), self.Filename, self.file_extension, util.get_UserID(), None) # None is for outEntityID
		results = cursor.callproc('spCreateEntity', args)
		self.EntityID = results[4]
		
		if self.EntityID == None:
			raise RuntimeError("uh oh, something went fucko when creating the entity")

	def _append_entity(self, entity_part):
		cursor = get_db().cursor()
		args = (self.EntityID, entity_part.get_FilePart_db(), entity_part.get_InsertOrder(), 3)
		results = cursor.callproc('spAppendEntity', args)
		entity_part.set_EntityPartID(results[3])

		if entity_part.get_EntityPartID() == None:
			raise RuntimeError("uh oh, something went fucko when creating the entity")




class EntityPart:

	def __init__(self, FilePart, InsertOrder, EntityPartID=None):
		self.EntityPartID = EntityPartID # None with new files
		self.InsertOrder = InsertOrder
		self.FilePart = FilePart

	# todo with defaults
	# def __init__(self, EntityPartID, InsertOrder, FilePart):
	# 	self.EntityPartID = EntityPartID
	# 	self.InsertOrder = InsertOrder
	# 	self.FilePart = FilePart

	def set_EntityPartID(self, EntityPartID):
		self.EntityPartID = EntityPartID

	def get_EntityPartID(self):
		return self.EntityPartID

	def get_FilePart_db(self):
		return binascii.hexlify(self.FilePart)

	def get_InsertOrder(self):
		return self.InsertOrder
