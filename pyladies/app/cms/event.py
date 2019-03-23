from flask import jsonify

from . import api
from ..exceptions import OK
from ..managers.event import Manager as EventManager


@api.route("/events", methods=["GET"])
def get_events():
    data = EventManager.get_events()

    info = {
        "code": OK.code,
        "message": OK.message
    }

    return jsonify(data=data, info=info)
