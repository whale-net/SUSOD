import datetime
import os
import threading
#import io
import time

import flask
import SUSOD

#@SUSOD.app.teardown_appcontext


class Cache():
	@property
	def cache_path(self):
		return self._cache_path

	@property
	def object_lifetime(self):
		return self._object_lifetime

	@property
	def cleanup_period(self):
		return self._cleanup_period

	@property
	def cache_lock_filename(self):
		return '.SUSOD.cache'

	def __init__(self):
		# cache at the entity-part level?

		# init properties
		self._cache_path = SUSOD.app.config['CACHE_FOLDER']
		self._cleanup_check_period = SUSOD.app.config['CACHE_CLEANUP_CHECK_PERIOD']
		self._object_lifetime = SUSOD.app.config['CACHE_OBJECT_LIFETIME']

		# init the timing mechanism - using a file's recent read time as clock
		# if this doesn't work with concurrent users we should probably doing somethin with our database
		self._cache_lock_file_path = os.path.join(self._cache_path, self.cache_lock_filename)
		if not os.path.exists(self._cache_lock_file_path):
			os.mknod(self._cache_lock_file_path)
		# TODO maybe improve this with touch_file function
		self._clean_time = datetime.datetime.fromtimestamp(os.path.getmtime(self._cache_lock_file_path))
		# trigger cache clean check. Will spawn thread if there is a cache to clean
		self.check_clean()
	
	# @cleanup_period.setter
	# def cleanup_period(self, cleanup_period):
	# 	self._cleanup_period = cleanup_period

	def check_clean(self, force_clean=False):
		now = datetime.datetime.now()
		# TODO need a separate timer for when we last checked
		if not force_clean and now - self._clean_time < self._cleanup_check_period:
			return
		else:
			threading.Thread(target=self.clean_cache).start()

	def clean_cache(self):
		# TODO this is here to prevent us from wiping the file that we are trying to access by creating the cache
		time.sleep(0.1);

		now = datetime.datetime.now()
		#print('CLEANIN')
		self.touch_file(self._cache_lock_file_path, touch_time=now)
		max_file_age = (now - self.object_lifetime).timestamp()

		for filename in os.listdir(self.cache_path):
			if filename == self.cache_lock_filename:	
				continue

			file_path = os.path.join(self.cache_path, filename)
			if os.stat(file_path).st_mtime < max_file_age:
				os.remove(file_path)


	def touch_file(self, filename, touch_time=None, create_if_not_found=True):
		if touch_time == None:
			touch_time = datetime.datetime.now()

		file_path = self.get_cache_file_path(filename)
		if os.path.exists(file_path):
			#print(file_path)
			os.utime(file_path, (touch_time.timestamp(), touch_time.timestamp()))
		else:
			if create_if_not_found:
				os.mknod(file_path)

	def get_cache_file_path(self, filename):
		return os.path.join(self.cache_path, filename)

	# def write_file(self, file_name, file_bytes):
	# 	if file_name == None:
	# 		file_name = "test.exe"
	# 	file_name = str(datetime.datetime.now()) + '_' + file_name
	# 	file_path = os.path.join(self.cache_path, file_name)

	# 	if 'OS' in os.environ:
	# 		print(file_path)
	# 		# Breaks in windows, unsure why

	# 	else:
	# 		with open(file_path, 'wb') as file:
	# 			file.write(bytearray(file_bytes))

class CacheFile():
	# manage an instance of a cache file
	@property
	def is_write_mode(self):
		return self._file_mode == 'ab' or self._file_mode == 'wb'

	@property
	def exists(self):
		return self._file_exists

	@property
	def file_path(self):
		return self._cache.get_cache_file_path(self._filename)
	

	def __init__(self, cache, filename):
		self._cache = cache
		self._filename = filename

	def __enter__(self):
		if os.path.exists(self.file_path):
			self._file_mode = 'rb'
			self._file_exists = True
			self._use_temp_filename = False
		else:
			self._file_mode = 'ab'
			self._file_exists = False
			self._use_temp_filename = True
			self._temp_filename = f'~{self._filename}'
			# delete existing temp file. Probably a bad idea for 2 concurrent requests for the same large uncached but we'll figure that out when we get there
			if os.path.exists(self._cache.get_cache_file_path(self._temp_filename)):
				os.remove(self._cache.get_cache_file_path(self._temp_filename))

		filename_to_use = self._filename
		if self._use_temp_filename:
			filename_to_use = self._temp_filename

		self._cache.touch_file(self._cache.get_cache_file_path(filename_to_use))
		self._file = open(self._cache.get_cache_file_path(filename_to_use), self._file_mode)

		# return the CacheFile object - make it behave similar to open
		return self

	def __exit__(self, type, value, traceback):
		if self._use_temp_filename:
			os.rename(self._cache.get_cache_file_path(self._temp_filename), self.file_path)
		self._file.close()

	def _upgrade_to_write_mode(self):
		if not self._file == None:
			self._file.close()
		self._file_mode = 'ab'
		self._file = open(self.file_path, self._file_mode)

	def write_chunk(self, file_bytes):
		if not self.is_write_mode:
			self._upgrade_to_write_mode()
		
		# TODO find better way of doing this (hash)
		self._file_exists = True

		#print(f'writing {len(file_bytes)} bytes')
		self._file.write(file_bytes)

	def refresh_file_delete_time(self):
		#print(f'refresh file delete time {self._filename}')
		self._cache.touch_file(self._filename, create_if_not_found=False)

	# def test(self):
	# 	print(f'CacheFile: {self._filename}')