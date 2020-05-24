import flask
import SUSOD
from SUSOD import util
from SUSOD.model import Entity

@SUSOD.app.route('/api/entity/<EntityID>', methods=['GET'])
@util.has_permissions
def api_entity_get(EntityID):
	e = Entity(EntityID)
	# TODO fix mimetype
	return flask.send_file(e.file_path(), attachment_filename=e.Filename)