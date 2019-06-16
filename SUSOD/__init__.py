"""
SUSOD package initilailiazation.

"""
import flask

app = flask.Flask(__name__)

app.config.from_object('SUSOD.config')

# disable for now but will be useful for dev/prod testing
# app.config.from_envvar('SUSOD_CONFIG', silent=True)

#http://flask.pocoo.org/docs/1.0/patterns/packages/
import SUSOD.controller
import SUSOD.model
import SUSOD.views