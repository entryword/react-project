from flask import jsonify, request

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


@api.route("/event", methods=["POST"])
def createEvent():
    request_data = request.get_json()

    data = request_data["data"]
    eventinfo = {
        "event_basic": {
            "topic_sn": data["topic_id"],
            "date": data["start_date"],
            # TODO:waiting table schema and data["end_date"] will add here
            "start_time": data["start_time"],
            "end_time": data["end_time"],
            "place_sn": data["place_id"],
        },
        "event_info": {
            "event_basic_sn": None,
            "title": data["title"],
            "desc": data["desc"],
            "fields": data["field_ids"],
            "speaker_sns": data["speaker_ids"],
            "assistant_sns": data["assistant_ids"],
        },
    }

    em = EventManager()
    event_basic_newid = em.create_event(eventinfo)
    res = {
        "data": {"id": event_basic_newid},
        "info": {"code": 0, "message": "Perform the action successfully."},
    }

    return jsonify(res)
