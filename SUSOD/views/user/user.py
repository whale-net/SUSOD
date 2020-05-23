"""
User view.
"""
import datetime
import flask
import SUSOD
from SUSOD import util
from SUSOD.model import Entity

@SUSOD.app.route('/user/login')
def show_user_login():
	""" Display /example page."""

	context = util.get_login_context()
	
	return flask.render_template('user/login.html', **context)

@SUSOD.app.route('/user/create')
def show_user_create():
	""" Display /example page."""

	context = util.get_login_context()
	
	return flask.render_template('user/create.html', **context)


@SUSOD.app.route('/user/')
@util.has_permissions
def show_user_index():
	""" Display /example page."""

	context = util.get_login_context()

	now = datetime.datetime.now()
	e = Entity(102)
	#e.file_path()
	new_now = datetime.datetime.now()
	print('getting ' , e.EntityID)
	print('\tDownload	: ', new_now - now)
	e.cache()
	really_now = datetime.datetime.now()
	print('\tWrite 		: ',  really_now - new_now)
	print('\tTotal time	: ', really_now - now)
		
	return flask.render_template('user/index.html', **context)