from flask import current_app, jsonify

from . import api
from ..exceptions import OK
from ..sqldb import DBWrapper
from ..utils import HashableDict
from app.managers.event import Manager as EventManager


@api.route("/event/<int:e_id>", methods=["GET"])
def get_event(e_id):
    if type(e_id) == int:
        EventService = EventManager()
        event_basic = EventService.get_event(e_id)

        info = {
            "code": OK.code,
            "message": OK.message
        }

        return jsonify(data=event_basic, info=info)
