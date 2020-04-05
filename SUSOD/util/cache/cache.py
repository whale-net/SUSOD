import datetime
import os

import flask
import SUSOD


class Cache():
	_global_cache = None

	def global_cache():
		if Cache._global_cache == None:
			Cache._global_cache = Cache(SUSOD.app.config['CACHE_FOLDER'],
										SUSOD.app.config['CACHE_CLEANUP_CHECK_PERIOD'],
										SUSOD.app.config['CACHE_LIFETIME'])
		Cache._global_cache.clean_cache()
		return Cache._global_cache

	def __init__(self, cache_path, cleanup_check_period, lifetime):
		self._cache_path = cache_path
		self._clean_time = datetime.datetime.now()
		self._cleanup_check_period = cleanup_check_period
		self._lifetime = lifetime

	@property
	def cache_path(self):
		return self._cache_path

	@property
	def lifetime(self):
		return self._lifetime

	@property
	def cleanup_period(self):
		return self._cleanup_period

	# @cleanup_period.setter
	# def cleanup_period(self, cleanup_period):
	# 	self._cleanup_period = cleanup_period

	def clean_cache(self):
		# check if we should clean
		print('clean check')
		now = datetime.datetime.now()
		if now - self._clean_time < self._cleanup_check_period:
			return
		print('CLEANING')
		self._clean_time = now

		max_file_age = (now - self.lifetime).timestamp()
		for file_name in os.listdir(self.cache_path):
			file_path = os.path.join(self.cache_path, file_name)
			if os.stat(file_path).st_mtime < max_file_age:
				print('REMOVING: ', file_path)
				os.remove(file_path)

	def write_file(self, file_name, file_bytes):
		if file_name == None:
			file_name = "test.exe"
		file_name = str(datetime.datetime.now()) + '_' + file_name
		file_path = os.path.join(self.cache_path, file_name)

		if 'OS' in os.environ:
			print(file_path)
			# Breaks in windows, unsure why

		else:
			with open(file_path, 'wb') as file:
				file.write(bytearray(file_bytes))
