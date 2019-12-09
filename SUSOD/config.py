"""
SUSOD dev config.
"""
import os
import datetime

APPLICATION_ROOT = '/'

SECRET_KEY = b'tobegenerated'
SESSION_COOKIE_NAME = 'login_name'

VAR_FOLDER = os.path.join(
	os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
	'var'
)

# Directory for file uploads
# currently not used
UPLOAD_FOLDER = os.path.join(
	VAR_FOLDER,
	'uploads'
)

CACHE_FOLDER = os.path.join(
	VAR_FOLDER,
	'cache'
)

CACHE_LIFETIME = datetime.timedelta(seconds=30) #datetime.timedelta(hours=24)
# Anything above this must be streamed and not put into cache
CACHE_MAX_FILE_SIZE = 1024 * 1024 * 64 
CACHE_CLEANUP_CHECK_PERIOD = datetime.timedelta(seconds=1)


# Database configuration
DATABASE_HOSTNAME = 'localhost'
DATABASE_NAME = 'dbSUSOD'
DATABASE_USERNAME = 'susod'
DATABASE_PASSWORD = 'password'

DATABASE_PORT = 3306
