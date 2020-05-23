import math
import datetime
import functools

import flask
from werkzeug.utils import secure_filename

import SUSOD
from SUSOD import model
from SUSOD import util


from ..db import *


class Entity:

	MAX_FILE_PART_SIZE = 16777216 - 1 # 16 MB / MEDIUMBLOB -> needs to be 1 byte less else sql connector goes dead

	def __init__(self, EntityID=None):
		self._EntityID = EntityID
		self._Description = None
		self._EntityTypeID = None
		self._Filename = None

		self._entity_parts = []

		if self.EntityID != None:
			self._init_entity()

	@property
	def EntityID(self):
		return self._EntityID

	@property
	def Description(self):
		return self._Description

	@property
	def EntityTypeID(self):
		return self._EntityTypeID

	@property
	def Filename(self):
		return self._Filename

	@property
	def filename_for_cache(self):
		return 'E' + str(self.EntityID)
	
	@property
	def is_entity_loaded(self):
		# is the entire entity loaded into memory
		if self.EntityID == None or len(self._entity_parts) == 0 or self.Filename == None or self.EntityTypeID == None:
			return False
		for entity_part in self._entity_parts:
			if not entity_part.is_loaded:
				return False
		return True

	# def get_file_size(self):
	# 	return self.file_size

	def file_path(self):
		self.cache()
		return self._file_path



	def cache(self):
		"""
		Caches the file on the local server and refreshes cache delete period
		"""
		with util.CacheFile(util.Cache(), self.filename_for_cache) as cache_file:
			if cache_file.exists:
				# TODO we have a race condition between the file existing and the touch. We need something more robust
				# for now it won't create the file with the touch so it errors instead of serving empty files
				cache_file.refresh_file_delete_time()
			else:
				self._load_entity()
				for entity_part in self._entity_parts:
					cache_file.write_chunk(entity_part.FilePart)

			self._file_path = cache_file.file_path

	def create(self, file, file_name=None):
		"""
		Take a file
		"""
		if file == None:
			raise ValueError("file is not valid")

		if self.EntityID != None:
			raise RuntimeError("Entity - Entity already exists")

		if file_name == None:
			try:
				file_name = file.filename
			except:
				file_name = None
		file_name = secure_filename(file_name)
		self._Filename = file_name

		# surely there has to be a better way to do this
		self._file_extension = self.Filename.split('.')[-1]
		if len(self._file_extension) > 5: # probably not an extension, made up number, can change or remove
			self._file_extension = None

		insert_start = datetime.datetime.now()
		
		buffer = file.read(Entity.MAX_FILE_PART_SIZE)
		insert_order = EntityPart.INSERT_ORDER_BEGIN
		while len(buffer) > 0:
			entity_part = EntityPart(FilePart=buffer, InsertOrder=insert_order, EntityID=self.EntityID)
			entity_part.write_to_db(Filename=self.Filename, file_extension=self._file_extension)
			self._EntityID = entity_part.EntityID
			self._entity_parts.append(entity_part)
			buffer = file.read(Entity.MAX_FILE_PART_SIZE)
			insert_order += 1

		self._file_size = sum([entity_part.Length for entity_part in self._entity_parts])
		
		print("""
Entity [{}] inserted in: {} 
	Bytes: {}
	Parts: {}
""".format(int(self.EntityID), (datetime.datetime.now() - insert_start), self._file_size, len(self._entity_parts))
)

		# todo handle deleting of entity on fail

	def _init_entity(self):
		# initialize all of our entity classes
		cursor = get_db().cursor()
		
		sql = """
			SELECT E.Filename, E.Description, E.EntityTypeID
			FROM Entitys E
			WHERE E.EntityID = (%s)
		"""
		cursor.execute(sql, (self.EntityID,))
		info_row = cursor.fetchall()[0]
		self._Filename = info_row[0]
		self._Description = info_row[1]
		self._EntityTypeID = int(info_row[2])


		sql = """
			SELECT EP.EntityPartID, EP.InsertOrder
			FROM EntityParts EP
			WHERE EP.EntityID = (%s)
			ORDER BY EP.InsertOrder
		"""
		cursor.execute(sql, (self.EntityID,))
		entity_part_rows = cursor.fetchall()
		print(entity_part_rows)

		for row in entity_part_rows:
			#entity_part = EntityPart(EntityPartID=row["EntityPartID"])
			entity_part = EntityPart(EntityPartID=row[0], InsertOrder=row[1])
			self._entity_parts.append(entity_part)
		self._entity_parts.sort()
		# money = 100
		# sql = "something with moeny"
		# with SuperTransaction() as tran:
		# 	sqlrow = SuperCursor(tran).execute(sql)
		# 	sqlrow['money'] *= 5
		# 	money = sqlrow['money']
		# 	SuperCursor(tran).execute_update(sqlrow)
		# return money

	def _load_entity(self):
		if self.is_entity_loaded:
			return

		for entity_part in self._entity_parts:
			entity_part.load_entity_part_from_db()

class EntityPart:

	# In case we ever want to prepend files?
	INSERT_ORDER_BEGIN = 1

	def __init__(self, FilePart=None, InsertOrder=None, EntityID=None, EntityPartID=None):
		self._EntityPartID = EntityPartID
		self._InsertOrder = InsertOrder

		if self.EntityPartID == None:
			self._FilePart = FilePart
			
			self._EntityID = EntityID

			self._Length = len(self._FilePart)

			if self.EntityID == None and self.InsertOrder == EntityPart.INSERT_ORDER_BEGIN:
				self._NewEntity = True
			else:
				self._NewEntity = False

	def __lt__(self, other):
		# for sorting a list of EntityParts
		return self.InsertOrder < other.InsertOrder

	@property
	def FilePart(self):
		if not hasattr(self, '_FilePart'):
			return None
		return self._FilePart
	
	@property
	def InsertOrder(self):
		return self._InsertOrder
	
	@property
	def EntityID(self):
		return self._EntityID
	
	@property
	def EntityPartID(self):
		return self._EntityPartID
	
	@property
	def Length(self):
		return self._Length

	@property
	def filename_for_cache(self):
		return 'EP' + str(self.EntityPartID)

	@property
	def is_loaded(self):
		# is the file chunk loaded into memory
		# definition of loaded will change if we ever stream chunks
		return self.FilePart != None

	def load_entity_part_from_db(self):
		cursor = get_db(raw=True).cursor()		
		sql = """
			SELECT EP.FilePart, EP.EntityID, EP.InsertOrder
			FROM EntityParts EP
			WHERE EP.EntityPartID = (%s)
		"""
		cursor.execute(sql, (self.EntityPartID,))
		results = cursor.fetchone()
		self._FilePart = results[0]
		self._EntityID = results[1]
		self._InsertOrder = results[2]

	def load_entity_part_from_bytearray(self, FilePart):
		cursor = get_db(raw=True).cursor()		
		sql = """
			SELECT EP.EntityID, EP.InsertOrder
			FROM EntityParts EP
			WHERE EP.EntityPartID = (%s)
		"""
		cursor.execute(sql, (self.EntityPartID,))
		results = cursor.fetchone()
		self._FilePart = FilePart
		self._EntityID = results[0]
		self._InsertOrder = results[1]		
	
	# todo with defaults
	# def __init__(self, EntityPartID, InsertOrder, FilePart):
	# 	self.EntityPartID = EntityPartID
	# 	self.InsertOrder = InsertOrder
	# 	self.FilePart = FilePart

	def write_to_db(self, Filename=None, file_extension=None):
		if self.EntityPartID != None:
			return (self.EntityID, self.EntityPartID)
		try:
			# setup cursor as needed, not initially so we don't get too many connections
			cursor = get_db(raw=True).cursor()
			if self._NewEntity:
				self._new_entity(cursor, Filename, file_extension)
			else:
				self._append_entity(cursor)
		except Exception as e:
			print(e)
			self._delete_from_db(cursor)
		finally:
			cursor.close()
		return (self.EntityID, self.EntityPartID)

			


	def _delete_from_db(self, cursor):
		# don't delete Entity here because of foreign keys
		cursor.execute("""DELETE FROM EntityParts WHERE EntityPartID = (%s)""", (self.EntityPartID,))

	def _new_entity(self, cursor, FileName, file_extension):
		print('New Entity Being Created @ [{}]'.format(str(datetime.datetime.now())))
		args = (self.FilePart, FileName, file_extension, util.get_UserID(), None, None) # None is for outEntityID, outEntityPartID
		self._sql_results = cursor.callproc('spCreateEntity', args)
		self._EntityID = int(self._sql_results[4])
		self._EntityPartID = int(self._sql_results[5])

		if self.EntityID == None:
			raise RuntimeError("uh oh, something went fucko when creating the entity")
		if self.EntityPartID == None:
			raise RuntimeError("uh oh, something went fucko when creating the entitypart")

		print('Entity [{}] was created @ [{}]'.format(self.EntityID, str(datetime.datetime.now())))

	def _append_entity(self, cursor):
		print('Entity [{}] writing Part [{}] @ [{}]'.format(self.EntityID, self.InsertOrder, str(datetime.datetime.now())))

		args = (self.EntityID, self.FilePart, self.InsertOrder, None)
		self._sql_results = cursor.callproc('spAppendEntity', args)
		self._EntityPartID = int(self._sql_results[3])

		if self.EntityPartID == None:
			raise RuntimeError("uh oh, something went fucko when creating the entity")
