"""
SUSOD dev config.

currently not very useful
"""

APPLICATION_ROOT = '/'

SECRET_KEY = b'tobegenerated'
SESSION_COOKIE_NAME = 'login_name'

# Directory for file uploads
# currently not used
UPLOAD_FOLDER = os.path.join(
	os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
	'var',
	'uploads',
)

# Database configuration
DATABASE_HOSTNAME = 'localhost'
DATABASE_NAME = 'susod'
DATABASE_USERNAME = 'susod_user'
DATABASE_PASSWORD = 'password'

