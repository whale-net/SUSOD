"""
SUSOD package initilailiazation.

"""
import flask
import os

app = flask.Flask(__name__)

app.config.from_object('SUSOD.config')

# disable for now but will be useful for dev/prod testing
# app.config.from_envvar('SUSOD_CONFIG', silent=True)

#http://flask.pocoo.org/docs/1.0/patterns/packages/
import SUSOD.controller
import SUSOD.model
import SUSOD.views
import SUSOD.util

if not os.path.exists(app.config['VAR_FOLDER']):
	os.mkdir(app.config['VAR_FOLDER'])

if not os.path.exists(app.config['CACHE_FOLDER']):
	os.mkdir(app.config['CACHE_FOLDER'])
