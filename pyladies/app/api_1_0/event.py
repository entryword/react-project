from flask import current_app, jsonify

from . import api
from ..exceptions import OK
from ..sqldb import DBWrapper
from ..utils import HashableDict
from app.managers.event import Manager as EventManager


#TODO: else case
@api.route("/event/<int:e_id>", methods=["GET"])
def get_event(e_id):
    event_service = EventManager()
    event_info = event_service.get_event(e_id)

    info = {
        "code": OK.code,
        "message": OK.message
    }

    return jsonify(data=event_info, info=info)